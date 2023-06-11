 /*********************************************************************
 * Software License Agreement (BSD License)
 *
 *  Copyright (c) 2011, Rice University
 *  All rights reserved.
 *
 *  Redistribution and use in source and binary forms, with or without
 *  modification, are permitted provided that the following conditions
 *  are met:
 *
 *   * Redistributions of source code must retain the above copyright
 *     notice, this list of conditions and the following disclaimer.
 *   * Redistributions in binary form must reproduce the above
 *     copyright notice, this list of conditions and the following
 *     disclaimer in the documentation and/or other materials provided
 *     with the distribution.
 *   * Neither the name of the Rice University nor the names of its
 *     contributors may be used to endorse or promote products derived
 *     from this software without specific prior written permission.
 *
 *  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
 *  "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
 *  LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
 *  FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
 *  COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
 *  INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
 *  BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
 *  LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
 *  CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
 *  LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
 *  ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 *  POSSIBILITY OF SUCH DAMAGE.
 *********************************************************************/
  
 /* Author: Luis G. Torres, Jonathan Gammell */
  
 #include <ompl/base/SpaceInformation.h>
 #include <ompl/base/objectives/PathLengthOptimizationObjective.h>
 #include <ompl/base/objectives/StateCostIntegralObjective.h>
 #include <ompl/base/objectives/MaximizeMinClearanceObjective.h>
 #include <ompl/base/spaces/RealVectorStateSpace.h>
 // For ompl::msg::setLogLevel
 #include "ompl/util/Console.h"
  
 // The supported optimal planners, in alphabetical order
 #include <ompl/geometric/planners/informedtrees/AITstar.h>
 #include <ompl/geometric/planners/informedtrees/BITstar.h>
 #include <ompl/geometric/planners/cforest/CForest.h>
 #include <ompl/geometric/planners/fmt/FMT.h>
 #include <ompl/geometric/planners/fmt/BFMT.h>
 #include <ompl/geometric/planners/prm/PRMstar.h>
 #include <ompl/geometric/planners/rrt/InformedRRTstar.h>
 #include <ompl/geometric/planners/rrt/RRTstar.h>
 #include <ompl/geometric/planners/rrt/SORRTstar.h>
  
  
 // For boost program options
 #include <boost/program_options.hpp>
 // For string comparison (boost::iequals)
 #include <boost/algorithm/string.hpp>
 // For std::make_shared
 #include <memory>
  
 #include <fstream>
  
  
 namespace ob = ompl::base;
 namespace og = ompl::geometric;
  
 // An enum of supported optimal planners, alphabetical order
 enum optimalPlanner
 {
     PLANNER_AITSTAR,
     PLANNER_BFMTSTAR,
     PLANNER_BITSTAR,
     PLANNER_CFOREST,
     PLANNER_FMTSTAR,
     PLANNER_INF_RRTSTAR,
     PLANNER_PRMSTAR,
     PLANNER_RRTSTAR,
     PLANNER_SORRTSTAR,
 };
  
 // An enum of the supported optimization objectives, alphabetical order
 enum planningObjective
 {
     OBJECTIVE_PATHCLEARANCE,
     OBJECTIVE_PATHLENGTH,
     OBJECTIVE_THRESHOLDPATHLENGTH,
     OBJECTIVE_WEIGHTEDCOMBO
 };
  
 // Parse the command-line arguments
 bool argParse(int argc, char** argv, double *runTimePtr, optimalPlanner *plannerPtr, planningObjective *objectivePtr, std::string *outputFilePtr);
  
 // Our "collision checker". For this demo, our robot's state space
 // lies in [0,1]x[0,1], with a circular obstacle of radius 0.25
 // centered at (0.5,0.5). Any states lying in this circular region are
 // considered "in collision".
 //我们的“碰撞检查器”。对于这个演示，我们的机器人的状态空间
//位于[0,1]x[0,1]，具有半径为0.25的圆形障碍物
//以（0.5,0.5）为中心。位于这个圆形区域的任何状态都是
//被视为“碰撞中”。
 class ValidityChecker : public ob::StateValidityChecker
 {
 public:
     ValidityChecker(const ob::SpaceInformationPtr& si) :
         ob::StateValidityChecker(si) {}
  
     // Returns whether the given state's position overlaps the
     // circular obstacle
     //返回给定状态的位置是否与
    //圆形障碍物
     bool isValid(const ob::State* state) const override
     {
         return this->clearance(state) > 0.0;
     }
  
     // Returns the distance from the given state's position to the
     // boundary of the circular obstacle.
     //返回从给定状态的位置到
    //圆形障碍物的边界。    
     double clearance(const ob::State* state) const override
     {
         // We know we're working with a RealVectorStateSpace in this
         // example, so we downcast state into the specific type.
         //我们知道我们正在使用RealVectorStateSpace
        //例如，因此我们将状态下转换为特定类型。
         const auto* state2D =
             state->as<ob::RealVectorStateSpace::StateType>();
  
         // Extract the robot's (x,y) position from its state
         double x = state2D->values[0];
         double y = state2D->values[1];
  
         // Distance formula between two points, offset by the circle's
         // radius
         return sqrt((x-0.5)*(x-0.5) + (y-0.5)*(y-0.5)) - 0.25;
     }
 };
  
 ob::OptimizationObjectivePtr getPathLengthObjective(const ob::SpaceInformationPtr& si);
  
 ob::OptimizationObjectivePtr getThresholdPathLengthObj(const ob::SpaceInformationPtr& si);
  
 ob::OptimizationObjectivePtr getClearanceObjective(const ob::SpaceInformationPtr& si);
  
 ob::OptimizationObjectivePtr getBalancedObjective1(const ob::SpaceInformationPtr& si);
  
 ob::OptimizationObjectivePtr getBalancedObjective2(const ob::SpaceInformationPtr& si);
  
 ob::OptimizationObjectivePtr getPathLengthObjWithCostToGo(const ob::SpaceInformationPtr& si);
  
 ob::PlannerPtr allocatePlanner(ob::SpaceInformationPtr si, optimalPlanner plannerType)
 {
     switch (plannerType)
     {
         case PLANNER_AITSTAR:
         {
             return std::make_shared<og::AITstar>(si);
             break;
         }
         case PLANNER_BFMTSTAR:
         {
             return std::make_shared<og::BFMT>(si);
             break;
         }
         case PLANNER_BITSTAR:
         {
             return std::make_shared<og::BITstar>(si);
             break;
         }
         case PLANNER_CFOREST:
         {
             return std::make_shared<og::CForest>(si);
             break;
         }
         case PLANNER_FMTSTAR:
         {
             return std::make_shared<og::FMT>(si);
             break;
         }
         case PLANNER_INF_RRTSTAR:
         {
             return std::make_shared<og::InformedRRTstar>(si);
             break;
         }
         case PLANNER_PRMSTAR:
         {
             return std::make_shared<og::PRMstar>(si);
             break;
         }
         case PLANNER_RRTSTAR:
         {
             return std::make_shared<og::RRTstar>(si);
             break;
         }
         case PLANNER_SORRTSTAR:
         {
             return std::make_shared<og::SORRTstar>(si);
             break;
         }
         default:
         {
             OMPL_ERROR("Planner-type enum is not implemented in allocation function.");
             return ob::PlannerPtr(); // Address compiler warning re: no return value.
             break;
         }
     }
 }
  
 ob::OptimizationObjectivePtr allocateObjective(const ob::SpaceInformationPtr& si, planningObjective objectiveType)
 {
     switch (objectiveType)
     {
         case OBJECTIVE_PATHCLEARANCE:
             return getClearanceObjective(si);
             break;
         case OBJECTIVE_PATHLENGTH:
             return getPathLengthObjective(si);
             break;
         case OBJECTIVE_THRESHOLDPATHLENGTH:
             return getThresholdPathLengthObj(si);
             break;
         case OBJECTIVE_WEIGHTEDCOMBO:
             return getBalancedObjective1(si);
             break;
         default:
             OMPL_ERROR("Optimization-objective enum is not implemented in allocation function.");
             return ob::OptimizationObjectivePtr();
             break;
     }
 }
  
// 定义一个函数plan，接受参数：运行时间(runTime)、规划器类型(plannerType)、规划目标类型(objectiveType)、输出文件名(outputFile)
void plan(double runTime, optimalPlanner plannerType, planningObjective objectiveType, const std::string& outputFile)
{
    // 构造一个二维实数向量状态空间，范围在[0,1]x[0,1]
    auto space(std::make_shared<ob::RealVectorStateSpace>(2));

    // 设置状态空间的边界为[0,1]
    space->setBounds(0.0, 1.0);

    // 构造一个用于检查状态空间中哪些状态是合法的SpaceInformation实例
    auto si(std::make_shared<ob::SpaceInformation>(space));

    // 设置状态合法性检查器为ValidityChecker类的实例
    si->setStateValidityChecker(std::make_shared<ValidityChecker>(si));

    si->setup();

    // 设置起始状态为环境的左下角(0,0)
    ob::ScopedState<> start(space);
    start->as<ob::RealVectorStateSpace::StateType>()->values[0] = 0.0;
    start->as<ob::RealVectorStateSpace::StateType>()->values[1] = 0.0;

    // 设置目标状态为环境的右上角(1,1)
    ob::ScopedState<> goal(space);
    goal->as<ob::RealVectorStateSpace::StateType>()->values[0] = 1.0;
    goal->as<ob::RealVectorStateSpace::StateType>()->values[1] = 1.0;

    // 创建问题实例
    auto pdef(std::make_shared<ob::ProblemDefinition>(si));

    // 设置起始状态和目标状态
    pdef->setStartAndGoalStates(start, goal);

    // 创建优化目标，根据传入的命令行参数来选择具体的目标类型
    // allocateObjective函数根据objectiveType参数返回一个优化目标对象
    pdef->setOptimizationObjective(allocateObjective(si, objectiveType));

    // 构造指定类型的优化规划器，根据传入的命令行参数来选择具体的规划器类型
    // allocatePlanner函数根据plannerType参数返回一个规划器对象
    ob::PlannerPtr optimizingPlanner = allocatePlanner(si, plannerType);

    // 设置问题实例给规划器来解决
    optimizingPlanner->setProblemDefinition(pdef);
    optimizingPlanner->setup();

    // 尝试在给定的运行时间内解决规划问题
    ob::PlannerStatus solved = optimizingPlanner->solve(runTime);

     if (solved)
     {
         // Output the length of the path found
         std::cout
             << optimizingPlanner->getName()
             << " found a solution of length "
             << pdef->getSolutionPath()->length()
             << " with an optimization objective value of "
             << pdef->getSolutionPath()->cost(pdef->getOptimizationObjective()) << std::endl;
  
         // If a filename was specified, output the path as a matrix to
         // that file for visualization
         if (!outputFile.empty())
         {
             std::ofstream outFile(outputFile.c_str());
             std::static_pointer_cast<og::PathGeometric>(pdef->getSolutionPath())->
                 printAsMatrix(outFile);
             outFile.close();
         }
     }
     else
         std::cout << "No solution found." << std::endl;
 }
  
 int main(int argc, char** argv)
 {
     // The parsed arguments
     double runTime;
     optimalPlanner plannerType;
     planningObjective objectiveType;
     std::string outputFile;
  
     // Parse the arguments, returns true if successful, false otherwise
     if (argParse(argc, argv, &runTime, &plannerType, &objectiveType, &outputFile))
     {
         // Plan
         plan(runTime, plannerType, objectiveType, outputFile);
  
         // Return with success
         return 0;
     }
     // Return with error
     return -1;
 }
  
 ob::OptimizationObjectivePtr getPathLengthObjective(const ob::SpaceInformationPtr& si)
 {
     return std::make_shared<ob::PathLengthOptimizationObjective>(si);
 }
  
 ob::OptimizationObjectivePtr getThresholdPathLengthObj(const ob::SpaceInformationPtr& si)
 {
     auto obj(std::make_shared<ob::PathLengthOptimizationObjective>(si));
     obj->setCostThreshold(ob::Cost(1.51));
     return obj;
 }
  
 class ClearanceObjective : public ob::StateCostIntegralObjective
 {
 public:
     ClearanceObjective(const ob::SpaceInformationPtr& si) :
         ob::StateCostIntegralObjective(si, true)
     {
     }
  
     // Our requirement is to maximize path clearance from obstacles,
     // but we want to represent the objective as a path cost
     // minimization. Therefore, we set each state's cost to be the
     // reciprocal of its clearance, so that as state clearance
     // increases, the state cost decreases.
     ob::Cost stateCost(const ob::State* s) const override
     {
         return ob::Cost(1 / (si_->getStateValidityChecker()->clearance(s) +
             std::numeric_limits<double>::min()));
     }
 };
  
 ob::OptimizationObjectivePtr getClearanceObjective(const ob::SpaceInformationPtr& si)
 {
     return std::make_shared<ClearanceObjective>(si);
 }
  
 ob::OptimizationObjectivePtr getBalancedObjective1(const ob::SpaceInformationPtr& si)
 {
     auto lengthObj(std::make_shared<ob::PathLengthOptimizationObjective>(si));
     auto clearObj(std::make_shared<ClearanceObjective>(si));
     auto opt(std::make_shared<ob::MultiOptimizationObjective>(si));
     opt->addObjective(lengthObj, 10.0);
     opt->addObjective(clearObj, 1.0);
  
     return ob::OptimizationObjectivePtr(opt);
 }
  
 ob::OptimizationObjectivePtr getBalancedObjective2(const ob::SpaceInformationPtr& si)
 {
     auto lengthObj(std::make_shared<ob::PathLengthOptimizationObjective>(si));
     auto clearObj(std::make_shared<ClearanceObjective>(si));
  
     return 10.0*lengthObj + clearObj;
 }
  
 ob::OptimizationObjectivePtr getPathLengthObjWithCostToGo(const ob::SpaceInformationPtr& si)
 {
     auto obj(std::make_shared<ob::PathLengthOptimizationObjective>(si));
     obj->setCostToGoHeuristic(&ob::goalRegionCostToGo);
     return obj;
 }
  
 bool argParse(int argc, char** argv, double* runTimePtr, optimalPlanner *plannerPtr, planningObjective *objectivePtr, std::string *outputFilePtr)
 {
     namespace bpo = boost::program_options;
  
     // Declare the supported options.
     bpo::options_description desc("Allowed options");
     desc.add_options()
         ("help,h", "produce help message")
         ("runtime,t", bpo::value<double>()->default_value(1.0), "(Optional) Specify the runtime in seconds. Defaults to 1 and must be greater than 0.")
         ("planner,p", bpo::value<std::string>()->default_value("RRTstar"), "(Optional) Specify the optimal planner to use, defaults to RRTstar if not given. Valid options are AITstar, BFMTstar, BITstar, CForest, FMTstar, InformedRRTstar, PRMstar, RRTstar, and SORRTstar.") //Alphabetical order
         ("objective,o", bpo::value<std::string>()->default_value("PathLength"), "(Optional) Specify the optimization objective, defaults to PathLength if not given. Valid options are PathClearance, PathLength, ThresholdPathLength, and WeightedLengthAndClearanceCombo.") //Alphabetical order
         ("file,f", bpo::value<std::string>()->default_value(""), "(Optional) Specify an output path for the found solution path.")
         ("info,i", bpo::value<unsigned int>()->default_value(0u), "(Optional) Set the OMPL log level. 0 for WARN, 1 for INFO, 2 for DEBUG. Defaults to WARN.");
     bpo::variables_map vm;
     bpo::store(bpo::parse_command_line(argc, argv, desc), vm);
     bpo::notify(vm);
  
     // Check if the help flag has been given:
     if (vm.count("help") != 0u)
     {
         std::cout << desc << std::endl;
         return false;
     }
  
     // Set the log-level
     unsigned int logLevel = vm["info"].as<unsigned int>();
  
     // Switch to setting the log level:
     if (logLevel == 0u)
     {
         ompl::msg::setLogLevel(ompl::msg::LOG_WARN);
     }
     else if (logLevel == 1u)
     {
         ompl::msg::setLogLevel(ompl::msg::LOG_INFO);
     }
     else if (logLevel == 2u)
     {
         ompl::msg::setLogLevel(ompl::msg::LOG_DEBUG);
     }
     else
     {
         std::cout << "Invalid log-level integer." << std::endl << std::endl << desc << std::endl;
         return false;
     }
  
     // Get the runtime as a double
     *runTimePtr = vm["runtime"].as<double>();
  
     // Sanity check
     if (*runTimePtr <= 0.0)
     {
         std::cout << "Invalid runtime." << std::endl << std::endl << desc << std::endl;
         return false;
     }
  
     // Get the specified planner as a string
     std::string plannerStr = vm["planner"].as<std::string>();
  
     // Map the string to the enum
     if (boost::iequals("AITstar", plannerStr)) {
         *plannerPtr = PLANNER_AITSTAR;
     }
     else if (boost::iequals("BFMTstar", plannerStr))
     {
         *plannerPtr = PLANNER_BFMTSTAR;
     }
     else if (boost::iequals("BITstar", plannerStr))
     {
         *plannerPtr = PLANNER_BITSTAR;
     }
     else if (boost::iequals("CForest", plannerStr))
     {
         *plannerPtr = PLANNER_CFOREST;
     }
     else if (boost::iequals("FMTstar", plannerStr))
     {
         *plannerPtr = PLANNER_FMTSTAR;
     }
     else if (boost::iequals("InformedRRTstar", plannerStr))
     {
         *plannerPtr = PLANNER_INF_RRTSTAR;
     }
     else if (boost::iequals("PRMstar", plannerStr))
     {
         *plannerPtr = PLANNER_PRMSTAR;
     }
     else if (boost::iequals("RRTstar", plannerStr))
     {
         *plannerPtr = PLANNER_RRTSTAR;
     }
     else if (boost::iequals("SORRTstar", plannerStr))
     {
         *plannerPtr = PLANNER_SORRTSTAR;
     }
     else
     {
         std::cout << "Invalid planner string." << std::endl << std::endl << desc << std::endl;
         return false;
     }
  
     // Get the specified objective as a string
     std::string objectiveStr = vm["objective"].as<std::string>();
  
     // Map the string to the enum
     if (boost::iequals("PathClearance", objectiveStr))
     {
         *objectivePtr = OBJECTIVE_PATHCLEARANCE;
     }
     else if (boost::iequals("PathLength", objectiveStr))
     {
         *objectivePtr = OBJECTIVE_PATHLENGTH;
     }
     else if (boost::iequals("ThresholdPathLength", objectiveStr))
     {
         *objectivePtr = OBJECTIVE_THRESHOLDPATHLENGTH;
     }
     else if (boost::iequals("WeightedLengthAndClearanceCombo", objectiveStr))
     {
         *objectivePtr = OBJECTIVE_WEIGHTEDCOMBO;
     }
     else
     {
         std::cout << "Invalid objective string." << std::endl << std::endl << desc << std::endl;
         return false;
     }
  
     // Get the output file string and store it in the return pointer
     *outputFilePtr = vm["file"].as<std::string>();
  
     // Looks like we parsed the arguments successfully
     return true;
 }