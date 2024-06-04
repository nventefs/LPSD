// Copyright (c) 2022 Applied Software Technology, Inc.

using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using nVentErico.LPSD.BaseClasses.Cvm;
using System;
using System.Collections.Generic;
using System.Linq;

namespace nVentErico.LPSD.Controllers.Cvm
{
    /// <summary> A class for obtaining Rationalized-Structure Data, 
    ///           the Collection Volume Up and Down Methods 
    ///           and Velocity-Derived Boundary point data. </summary>
    public class CvmEngine : CvmBase
    {
        #region Member Properties

        /// <summary> Gets or sets the JSON request. </summary>
        public CVMData Request { get; set; }

        /// <summary> Gets or sets the edge analysis data. </summary>
        public AnalysisEdge_CVM RequestAnalysisEdge { get; set; }

        /// <summary> Gets or sets the JSON response. </summary>
        public string Response { get; set; }

        /// <summary> Gets or sets the buildings. </summary>
        public IList<Building> Buildings { get; set; } = new List<Building>();

        /// <summary> Gets or sets the site object from the JSON data. </summary>
        public Site Site { get; set; }

        /// <summary> Gets or sets the web cookie from the CVM Controller. </summary>
        public dynamic UserCookie { get; set; }

        /// <summary> Gets the constant: electrical epsilon. </summary>
        public double ElectricalEpsilon { get; } = 8.85E-12;

        #endregion Member Properties

        #region Constructors

        /// <summary> Empty Default Constructor. </summary>
        public CvmEngine() : base() //base(1, KiCalculationType.Multiplicative, false, false)
        {

        }

        /// <summary> Main Constructor. </summary>
        ///
        /// <exception cref="Exception"> Thrown when an exception error condition occurs. </exception>
        ///
        /// <param name="json"> The JObject JSON object from the CVM Controller. </param>
        /// <param name="userCookie"> The web cookie from the CVM Controller. </param>
        public CvmEngine(JObject json, dynamic userCookie) : base() //base(1, KiCalculationType.Multiplicative, false, false)
        {
            try
            {
                UserCookie = userCookie;
                var jsonStr = JsonConvert.SerializeObject(json, LPSDJsonSerializationSettings.Singleton);
                Request = JsonConvert.DeserializeObject<CVMData>(jsonStr, LPSDJsonSerializationSettings.Singleton);
                RequestAnalysisEdge = JsonConvert.DeserializeObject<AnalysisEdge_CVM>(jsonStr, LPSDJsonSerializationSettings.Singleton);
                Buildings = Request.Buildings;

                var levels = Request.Levels.ToList();
                levels.ForEach(l => l.BoundingBox.MinimumWidth = BoundingBox.CalculateMinimumWidth(l.ConvexHullPoints));

                Site = Request.Site;
                if (Request != null)
                {
                    Request.Buildings = RationalizeGeometryFromRequest();
                    Buildings = Request.Buildings;
                    InitCvmData(Request);
                }
            }
            catch (Exception ex)
            {
                string className = "CvmEngine";
                string methodName = "CvmEngine Main Constructor";
                LogReport report = new LogReport(className, methodName, LogLevel.High, ex.Message, ex.StackTrace, UserCookie, new { json });
                report.WriteReport();
            }
        }

        /// <summary> Constructor. </summary>
        ///
        /// <exception cref="Exception"> Thrown when an exception error condition occurs. </exception>
        ///
        /// <param name="jsonStr"> The JSON string. </param>
        public CvmEngine(string jsonStr) : base() //base(1, KiCalculationType.Multiplicative, true, true)
        {
            try
            {
                Request = JsonConvert.DeserializeObject<CVMData>(jsonStr, LPSDJsonSerializationSettings.Singleton);
                RequestAnalysisEdge = JsonConvert.DeserializeObject<AnalysisEdge_CVM>(jsonStr, LPSDJsonSerializationSettings.Singleton);
                Buildings = Request.Buildings.ToList();
                Site = Request.Site;
                if (Request != null)
                {
                    Request.Buildings = RationalizeGeometryFromRequest();
                    Buildings = Request.Buildings;
                }
            }
            catch (Exception ex)
            {
                string className = "CvmEngine";
                string methodName = "CvmEngine Ctor";
                LogReport report = new LogReport(className, methodName, LogLevel.High, ex.Message, ex.StackTrace, UserCookie, new { jsonStr });
                report.WriteReport();
            }
        }

        #endregion Constructors

        #region Initialize CVM Data from JSON Request

        /// <summary> Begins the CVM calculations from the request JSON data . </summary>
        ///
        /// <param name="data"> The data. </param>
        public void InitCvmData(CVMData data)
        {
            try
            {
                //var terminalsResults = new List<Terminal>();
                List<Building> otherBldgs = new List<Building>();

                foreach (var building in Buildings.ToList())
                {
                    otherBldgs = Buildings.Where(b => !b.Guid.Equals(building.Guid)).Select(b => b).ToList();

                    var containsSubBuildings = otherBldgs.Where(b => b.Name.Contains('.')).Any();
                    if (containsSubBuildings && building.IsSubBuilding)
                    {
                        var parentBldgName = building.Name.Remove(building.Name.Length - 2);
                        var parentBldg = Buildings.Where(b => b.Name.Equals(parentBldgName)).Select(b => b).FirstOrDefault();

                        if (parentBldg != null)
                        {
                            otherBldgs = Buildings.Where(b => !b.Guid.Equals(building.Guid) && !b.Guid.Equals(parentBldg.Guid)).Select(b => b).ToList();
                        }
                        else
                        {
                            otherBldgs = Buildings.Where(b => !b.Guid.Equals(building.Guid)).Select(b => b).ToList();
                        }
                    }
                }

                foreach (var building in Buildings.ToList())
                {
                    otherBldgs = Buildings.Where(b => !b.Guid.Equals(building.Guid)).Select(b => b).ToList();

                    foreach (var level in building.Levels.ToList())
                    {
                        // Calculated CVM data for the dynaspheres
                        foreach (var requestTerminal in level.DynosphereAirTerminals.ToList())
                        {
                            // the request terminal to be modified by the newly created CVM data
                            //var requestTerminal = Request.Terminals.Where(t => t.Method == "Collection Volume" || t.Method == "CVM" && t.TerminalGuid == terminal.TerminalGuid).FirstOrDefault();

                            // Get the Ki and CVM Data for this terminal
                            //var terminalFromKiEngine = GetKiForDynasphere(building, requestTerminal.Level, requestTerminal, Site);
                            var terminalFromKiEngine = GetKiDataForDynasphere(building,
                                                                              building.BaseLevel,
                                                                              otherBldgs,
                                                                              requestTerminal,
                                                                              Site,
                                                                              requestTerminal.PoiPoint);

                            double z_m = CvmUp(terminalFromKiEngine.BreakDownE_Field,
                                               terminalFromKiEngine.Q_LeaderCharge,
                                               terminalFromKiEngine.CloudBase);

                            double d_s = CvmDown(terminalFromKiEngine.KiData.TotalKiContribution,
                                                 terminalFromKiEngine.BreakDownE_Field,
                                                 terminalFromKiEngine.Q_LeaderCharge,
                                                 terminalFromKiEngine.CloudBase);

                            // set the request terminals CVM values for the response object
                            var A_rResult = GetAttractiveRadius(z_m, d_s, terminalFromKiEngine.Top.Z, requestTerminal);

                            A_rResult = GetVelocityBoundaryPoints(z_m, requestTerminal, A_rResult);

                            //-Multiplicative factor for Ki
                            requestTerminal.TotalMultiplicative = terminalFromKiEngine.KiData.TotalMultiplicativeKiOnStructure;

                            //- Reductive factor for Ki
                            requestTerminal.TotalReductive = terminalFromKiEngine.KiData.TotalReductiveFactorOnStructure;

                            //-Ki of the terminal
                            requestTerminal.KiTotalContribution = terminalFromKiEngine.KiData.TotalKiContribution;

                            //- Height above ground of protection radius, zr
                            requestTerminal.HeightOfAttractiveRadius = A_rResult.Z_r;

                            //- Protection radius, Ra
                            requestTerminal.AttractiveRadius = A_rResult.AttractiveRadius;

                            //- Striking Distance
                            requestTerminal.StrikingDistance = d_s;

                            //- 6 Points along the Velocity Derived Boundary curve
                            requestTerminal.VelocityBoundaryPoints = A_rResult.VDB_Points;

                            //terminalsResults.Add(requestTerminal);
                        }

                        var pointsToEvaluate = level.PointsByLevelGuid.Where(p => !p.IsFaceHorizontal && !p.IsFaceVertical).Select(p => p).ToList();

                        // Calculated CVM data for the Corner POIs
                        foreach (var pointToEvaluate in pointsToEvaluate)
                        {

                            // Get the Ki and CVM Data
                            //var pointFromKiEngine = GetKiForPoint(building, level, point, Site);
                            Point pointFromKiEngine = GetKiDataForPoint(building,
                                                                        building.BaseLevel,
                                                                        otherBldgs,
                                                                        Site,
                                                                        pointToEvaluate);

                            double z_m = CvmUp(pointFromKiEngine.BreakDownE_Field,
                                               pointFromKiEngine.Q_LeaderCharge,
                                               pointFromKiEngine.CloudBase);

                            double d_s = CvmDown(pointFromKiEngine.KiData.TotalKiContribution,
                                                 pointFromKiEngine.BreakDownE_Field,
                                                 pointFromKiEngine.Q_LeaderCharge,
                                                 pointFromKiEngine.CloudBase);

                            // set the request corner point's CVM values for the response object
                            var A_rResult = GetAttractiveRadius(z_m, d_s, pointFromKiEngine.Position.Z);

                            //-Multiplicative factor for Ki
                            pointToEvaluate.TotalMultiplicative = pointFromKiEngine.KiData.TotalMultiplicativeKiOnStructure;

                            //- Reductive factor for Ki
                            pointToEvaluate.TotalReductive = pointFromKiEngine.KiData.TotalReductiveFactorOnStructure;

                            //-Ki of the Point
                            pointToEvaluate.KiTotalContribution = pointFromKiEngine.KiData.TotalKiContribution;

                            //- Height above ground of protection radius, zr
                            pointToEvaluate.HeightOfAttractiveRadius = A_rResult.Z_r;

                            //- Protection radius, Ra
                            pointToEvaluate.AttractiveRadius = A_rResult.AttractiveRadius;

                            //- Record the slope for comparisons
                            pointToEvaluate.Slope = pointFromKiEngine.Slope;
                        }

                        var edgePoints = new List<Point>();


                        if (level.LevelShape == LevelShape.Rectangle)
                        {
                            foreach (var point in level.Corners?.ToList())
                            {
                                SetKiForPointOnThisLevel(building, level, point);
                            }

                            foreach (var point in level.EdgePointsRectangular?.ToList())
                            {
                                SetKiForPointOnThisLevel(building, level, point);
                            }
                        }
                        if (level.LevelShape == LevelShape.Oval)
                        {
                            foreach (var point in level.EdgePointsOval?.ToList())
                            {
                                SetKiForPointOnThisLevel(building, level, point);
                            }
                        }
                        if (level.LevelShape == LevelShape.Gable)
                        {
                            foreach (var point in level.GableSlopedEdges?.ToList())
                            {
                                SetKiForPointOnThisLevel(building, level, point);
                            }
                        }
                    }
                }

                Response = JsonConvert.SerializeObject(Request, Formatting.Indented, new JsonSerializerSettings
                {
                    ReferenceLoopHandling = ReferenceLoopHandling.Ignore
                });
            }
            catch (Exception ex)
            {
                string className = "CvmEngine";
                string methodName = "InitCvmData";
                LogReport report = new LogReport(className, methodName, LogLevel.High, ex.Message, ex.StackTrace, UserCookie, new { data });
                report.WriteReport();
            }
        }

        private void SetKiForPointOnThisLevel(Building building, Level level, Point point)
        {
            try
            {
                // the request edge point to be modified by the newly created CVM data
                var requestPoint = Request.Points.Where(p => p.PointGuid == point?.PointGuid).FirstOrDefault();

                var otherBldgs = Buildings.Where(b => !b.Guid.Equals(building.Guid)).Select(b => b).ToList();

                // Get the Ki and CVM Data
                //var pointFromKiEngine = GetKiForPoint(building, level, point, Site);
                Point pointFromKiEngine = GetKiDataForPoint(building,
                                                            building.BaseLevel,
                                                            otherBldgs,
                                                            Site,
                                                            point);

                double z_m = CvmUp(pointFromKiEngine.BreakDownE_Field,
                                   pointFromKiEngine.Q_LeaderCharge,
                                   pointFromKiEngine.CloudBase);

                double d_s = CvmDown(pointFromKiEngine.KiData.TotalKiContribution,
                                     pointFromKiEngine.BreakDownE_Field,
                                     pointFromKiEngine.Q_LeaderCharge,
                                     pointFromKiEngine.CloudBase);

                // set the request edge point's CVM values for the response object
                var A_rResult = GetAttractiveRadius(z_m, d_s, pointFromKiEngine.Position.Z);

                //-Multiplicative factor for Ki
                requestPoint.TotalMultiplicative = pointFromKiEngine.KiData.TotalMultiplicativeKiOnStructure;

                //- Reductive factor for Ki
                requestPoint.TotalReductive = pointFromKiEngine.KiData.TotalReductiveFactorOnStructure;

                //-Ki of the Point
                requestPoint.KiTotalContribution = pointFromKiEngine.KiData.TotalKiContribution;

                //- Height above ground of protection radius, zr
                requestPoint.HeightOfAttractiveRadius = A_rResult.Z_r;

                //- Protection radius, Ra
                requestPoint.AttractiveRadius = A_rResult.AttractiveRadius;
            }
            catch (Exception ex)
            {
                throw ex;
            }
        }
        #endregion Initialize CVM Data from JSON Request

        #region Rationalize Building's Geometry



        /// <summary> Generates a building and level geometry from the request JSON data. </summary>
        public void GenerateGeometryFromRequest()
        {
            try
            {
                var allLevels = Request.Levels.Where(l => l.ForgeLevelElevation > 0.0).Select(l => l).ToList();
                List<Building> cvmBuildingData = new List<Building>();


                foreach (var building in Buildings)
                {
                    #region Set values from points and terminals for this building

                    building.H_Site = Convert.ToDouble(Request.Site.SiteElevation);

                    List<Level> levelsThisBuilding = new List<Level>();
                    List<Level> requestLevels = new List<Level>();
                    List<Point> pointsThisBuilding = new List<Point>();
                    List<Terminal> terminalsThisBuilding = new List<Terminal>();

                    if (building.IsSubBuilding)
                    {
                        levelsThisBuilding = GetBuildingLevelByPoints(pointsThisBuilding, allLevels);

                        foreach (var level in levelsThisBuilding.ToList())
                        {
                            var pointsThisLevel = Request.Points.Where(p => p.LevelGuid == level.LevelGuid).Select(p => p).ToList();
                            if (pointsThisLevel.Count() > 0)
                            {
                                pointsThisBuilding.AddRange(pointsThisLevel);
                            }
                        }

                        terminalsThisBuilding = Request.Terminals.Where(t => t.HostDesignModelGuid == building.Guid).Select(t => t).ToList();
                    }
                    else
                    {
                        pointsThisBuilding = Request.Points.Where(p => p.HostGuid == building.Guid).Select(p => p).ToList();
                        terminalsThisBuilding = Request.Terminals.Where(t => t.HostDesignModelGuid == building.Guid).Select(t => t).ToList();
                        levelsThisBuilding = Request.Levels.Where(l => l.HostGuid == building.Guid).Select(l => l).ToList();
                    }

                    //var cornerZValues = Request.Points.Where(p => p.IsCorner == true).Select(p => Math.Round(p.BottomPoint.Z, 1)).ToList();
                    //var cornerZValues = pointsThisBuilding.Where(p => p.IsCorner == true).Select(p => Math.Round(p.Position.Z, MidpointRounding.ToZero)).ToList();
                    var cornersbyZValues = pointsThisBuilding.Where(p => p.IsCorner == true).Select(p => Math.Floor(p.BottomPoint.Z)).Select(p => p).ToList();

                    // All dynaspheres
                    var dynaspheresThisBuilding = terminalsThisBuilding.Where(t => t.Method == "Collection Volume" || t.Method == "CVM").Select(p => p).ToList();

                    // All passive terminals
                    var passiveTerminalsThisBuilding = terminalsThisBuilding.Where(t => t.Method == "ESE").Select(p => p).ToList();

                    var analysisEdgeData = RequestAnalysisEdge.points;

                    Dictionary<string, List<AnalysisEdge_CVM>> analysisEdges = Point.IdentifyEdges_CVM(levelsThisBuilding, pointsThisBuilding, null);

                    //var levelElevationsByAnalysisEdge = analysisEdges.Keys.ToList();

                    // All unique corner Z values
                    var distinctCornerZValues = cornersbyZValues.Distinct().ToList();

                    // Order all unique corner Z values ascending
                    var levelElevationsByCornerPoints = distinctCornerZValues.OrderByDescending(cZ => cZ).ToArray();

                    // Number of levels by points
                    var levelsByPointsCount = levelElevationsByCornerPoints.Count();

                    //var buildingData = CreateBuildingWithLevels(building, pointsThisBuilding, passiveirTerminals, dynasphereAirTerminals, requestLevels, analysisEdges);
                    var buildingData = CreateBuildingPointData(building,
                                                               pointsThisBuilding,
                                                               passiveTerminalsThisBuilding,
                                                               dynaspheresThisBuilding,
                                                               levelsThisBuilding,
                                                               analysisEdges);

                    cvmBuildingData.Add(buildingData);

                    #endregion Set values from points and terminals 
                }

                Request.Buildings = cvmBuildingData;
            }
            catch (Exception ex)
            {
                string className = "CvmEngine";
                string methodName = "GenerateGeometryFromRequest";
                LogReport report = new LogReport(className, methodName, LogLevel.High, ex.Message, ex.StackTrace, UserCookie, null);
                report.WriteReport();
            }
        }

        /// <summary> Rationalizes geometry from request JSON data. </summary>
        public IList<Building> RationalizeGeometryFromRequest()
        {
            try
            {
                //var all_LevelGuids = Request.Levels.Select(l => l.HostGuid).ToList();

                var allLevels = Request.Levels.Where(l => l.ForgeLevelElevation > 0.0).Select(l => l).ToList();

                List<Level> levelsThisBuilding = new List<Level>();
                List<Level> requestLevels = new List<Level>();
                List<Point> pointsThisBuilding = new List<Point>();
                List<Terminal> terminalsThisBuilding = new List<Terminal>();

                List<Building> cvmBuildingData = new List<Building>();

                var buildingsWithPoints = Buildings.Where(b => Request.Points.Where(p => p.HostGuid == b.Guid).Count() > 0).ToArray();

                foreach (var building in buildingsWithPoints)
                {
                    if (building.IsSubBuilding)
                    {
                        var charIndex = building.Name.IndexOf(".");
                        var parentBldgLetter = building.Name.Remove(charIndex);
                        var parentBldg = Buildings.Where(b => b.Name.Equals(parentBldgLetter)).FirstOrDefault();
                        if (parentBldg != null)
                        {
                            var allLevelsThisBuilding = allLevels.Where(l => (l.HostGuid.Equals(parentBldg.Guid)) || l.HostGuid == building.Guid).Select(l => l).ToList();
                            pointsThisBuilding = Request.Points.Where(p => p.HostGuid == building.Guid).Select(p => p).ToList();
                            terminalsThisBuilding = Request.Terminals.Where(t => t.HostDesignModelGuid == building.Guid).Select(t => t).ToList();
                            levelsThisBuilding = GetBuildingLevelByPoints(pointsThisBuilding, allLevelsThisBuilding);
                        }
                    }
                    else
                    {
                        pointsThisBuilding = Request.Points.Where(p => p.HostGuid == building.Guid).Select(p => p).ToList();
                        terminalsThisBuilding = Request.Terminals.Where(t => t.HostDesignModelGuid == building.Guid).Select(t => t).ToList();
                        levelsThisBuilding = Request.Levels.Where(l => l.HostGuid == building.Guid).Select(l => l).ToList();
                    }

                    #region Set values from points and terminals for this building

                    building.H_Site = Convert.ToDouble(Request.Site.SiteElevation);

                    // All Corners
                    var cornersbyZValues = pointsThisBuilding.Where(p => p.IsCorner == true).Select(p => Math.Floor(p.BottomPoint.Z)).Select(p => p).ToList();

                    // All dynaspheres
                    var dynaspheresThisBuilding = terminalsThisBuilding.Where(t => t.Method == "Collection Volume" || t.Method == "CVM").Select(p => p).ToList();

                    // All passive terminals
                    var passiveTerminalsThisBuilding = terminalsThisBuilding.Where(t => t.Method == "ESE").Select(p => p).ToList();

                    var analysisEdgeData = RequestAnalysisEdge.points;

                    Dictionary<string, List<AnalysisEdge_CVM>> analysisEdges = Point.IdentifyEdges_CVM(levelsThisBuilding, pointsThisBuilding, null);

                    //var levelElevationsByAnalysisEdge = analysisEdges.Keys.ToList();

                    //var buildingData = CreateBuildingWithLevels(building, pointsThisBuilding, passiveirTerminals, dynasphereAirTerminals, requestLevels, analysisEdges);
                    var buildingData = CreateBuildingPointData(building,
                                                               pointsThisBuilding,
                                                               passiveTerminalsThisBuilding,
                                                               dynaspheresThisBuilding,
                                                               levelsThisBuilding,
                                                               analysisEdges);

                    cvmBuildingData.Add(buildingData);

                    #endregion Set values from points and terminals 
                }

                return cvmBuildingData;
            }
            catch (Exception ex)
            {
                string className = "CvmEngine";
                string methodName = "GenerateGeometryFromRequest";
                LogReport report = new LogReport(className, methodName, LogLevel.High, ex.Message, ex.StackTrace, UserCookie, null);
                report.WriteReport();
                return Request.Buildings;
            }
        }

        /// <summary> Gets building level by points. </summary>
        ///
        /// <param name="bldgePoints"> The bldge points. </param>
        /// <param name="possibleLevels"> The possible levels. </param>
        private List<Level> GetBuildingLevelByPoints(List<Point> bldgePoints, List<Level> possibleLevels)
        {
            var bldgLevels = new List<Level>();

            try
            {
                var distinctLevelGuids = bldgePoints.Select(p => p.LevelGuid).ToList().Distinct();

                foreach (var level in possibleLevels)
                {
                    if (distinctLevelGuids.Contains(level.LevelGuid))
                    {
                        bldgLevels.Add(level);
                    }
                }

            }
            catch (Exception ex)
            {
                string className = "CvmEngine";
                string methodName = "GetBuildingLevelByPoints";
                LogReport report = new LogReport(className, methodName, LogLevel.High, ex.Message, ex.StackTrace, UserCookie, null);
                report.WriteReport();

            }

            return bldgLevels;
        }

        public Building CreateBuildingPointData(Building building,
                                                List<Point> pointsThisBuilding,
                                                List<Terminal> passiveAirTerminals,
                                                List<Terminal> dynasphereAirTerminals,
                                                List<Level> forgeLevels,
                                                Dictionary<string, List<AnalysisEdge_CVM>> analysisEdges)
        {
            try
            {
                var comperisonTolerance = 1.5D;
                var pointDistanceToCheck = 1.75D;

                var levels = new List<Level>();
                var pointsThisLevel = new List<Point>();

                List<Level> allLevels = forgeLevels.Where(l => l.IsSubLevel == false).OrderByDescending(l => l.ForgeLevelElevation).Select(l => l).ToList();
                List<Level> allsublevels = forgeLevels.Where(l => l.IsSubLevel == true).OrderByDescending(l => l.ForgeLevelElevation).Select(l => l).ToList();

                var lowestLevelElevation = allLevels.Count > 0 ? allLevels.Select(l => l.ForgeLevelElevation).Min() : 0;
                var lowestLevel = allLevels.Where(l => l.ForgeLevelElevation == lowestLevelElevation).FirstOrDefault() ?? forgeLevels.OrderBy(l => l.ForgeLevelElevation).FirstOrDefault();

                Dictionary<string, Level> levelsByGuidDict = new Dictionary<string, Level>();
                forgeLevels.ForEach(fl => levelsByGuidDict.Add(fl.LevelGuid, fl));

                if (lowestLevel != null)
                {
                    building.BaseLevel = lowestLevel;

                    List<Level> levelsAbove = levelsByGuidDict.Values.Where(level => lowestLevel.LevelsAbove.Contains(level.LevelGuid)).ToList();
                    List<Level> levelStackAscending = levelsAbove;

                    List<Level> levelStackDecending = levelsAbove;

                    // Descending level stack by Forge elevation
                    levelStackDecending.Reverse();

                    // Add the lowest level to the list of levels to process
                    levelStackDecending.Add(lowestLevel);

                    foreach (var thisLevel in forgeLevels.ToList())
                    {
                        // Identify Sub-Level Parents
                        thisLevel.IsSubLevelParent = allsublevels.Where(l => l.ParentLevelGuid == thisLevel.LevelGuid &&
                                                     Math.Floor(l.ForgeLevelElevation) <= Math.Floor(thisLevel.ForgeLevelElevation) + comperisonTolerance).Any();

                        thisLevel.LevelsBelow = levelStackDecending.Where(l => l.ForgeLevelElevation < thisLevel.ForgeLevelElevation).Select(l => l.LevelGuid).ToList();
                        thisLevel.LevelsAbove = levelStackAscending.Where(l => l.ForgeLevelElevation > thisLevel.ForgeLevelElevation).Select(l => l.LevelGuid).ToList();

                        // get the lowest level and set its HeightJustThisLevel elevation
                        if (thisLevel.LevelGuid == lowestLevel.LevelGuid)
                        {
                            thisLevel.HeightJustThisLevel = thisLevel.ForgeLevelElevation;
                        }

                        foreach (var levelBelowGuid in thisLevel.LevelsBelow.ToList())
                        {
                            Level levelBelow = levelsByGuidDict[levelBelowGuid];
                            if (!thisLevel.IsSubLevelParent)
                            {
                                if (levelBelow.IsSubLevelParent)
                                {
                                    // There are no dynaspheres or points on these levels
                                    break;
                                }
                                if (thisLevel.IsSubLevel)
                                {
                                    // find sub-level below this one
                                    if (levelBelow.IsSubLevel)
                                    {
                                        // Is levelBelow below this sub-level
                                        var siblingSubLevles = thisLevel.LevelsBelow.Where(l => forgeLevels.Find(fl => fl.LevelGuid == l)?.ParentLevelGuid == levelBelow.ParentLevelGuid).ToList();

                                        if (siblingSubLevles.Count > 0)
                                        {
                                            // Find the sub-level below this one:
                                            foreach (var siblingSubLevelGuid in siblingSubLevles.ToList())
                                            {
                                                var siblingSubLevel = levelsByGuidDict[siblingSubLevelGuid];
                                                // get the centroid of this level's bounding box.
                                                thisLevel.BoundingBox.SetCentroidAndPoints(thisLevel.BoundingBox.MaxPoint, thisLevel.BoundingBox.MinPoint, thisLevel.ConvexHullPoints);
                                                siblingSubLevel.BoundingBox.SetCentroidAndPoints(siblingSubLevel.BoundingBox.MaxPoint, siblingSubLevel.BoundingBox.MinPoint, siblingSubLevel.ConvexHullPoints);

                                                if (thisLevel.BoundingBox.BoundingBoxPoints.Count > 3 && thisLevel.BoundingBox.BoundingBoxCentroid != null
                                                                                                      && siblingSubLevel.BoundingBox.BoundingBoxPoints.Count > 3)
                                                {
                                                    var isOverThisSiblingSubLevel = threeVector3.IsPointInPolygon(siblingSubLevel.BoundingBox.BoundingBoxPoints.ToArray(), thisLevel.BoundingBox.BoundingBoxCentroid);

                                                    if (isOverThisSiblingSubLevel)
                                                    {
                                                        thisLevel.HasLevelBelow = true;
                                                        thisLevel.NextLevelBelow = siblingSubLevel;
                                                        thisLevel.HeightJustThisLevel = thisLevel.ForgeLevelElevation - thisLevel.NextLevelBelow.ForgeLevelElevation;
                                                        break;
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                                else
                                {
                                    thisLevel.NextLevelBelow = levelsByGuidDict[levelBelowGuid];
                                    thisLevel.HeightJustThisLevel = thisLevel.ForgeLevelElevation - thisLevel.NextLevelBelow.ForgeLevelElevation;
                                    break;
                                }
                                if (thisLevel.HasLevelBelow == true && thisLevel.NextLevelBelow != null)
                                {
                                    break;
                                }
                                // If it is not a sub-level parent or a sub-level then it must be level without sub-levels
                                if (!levelsByGuidDict[levelBelowGuid].IsSubLevel && !levelsByGuidDict[levelBelowGuid].IsSubLevelParent)
                                {
                                    thisLevel.NextLevelBelow = levelsByGuidDict[levelBelowGuid];
                                    thisLevel.HeightJustThisLevel = thisLevel.ForgeLevelElevation - thisLevel.NextLevelBelow.ForgeLevelElevation;
                                    break;
                                }
                                if (!thisLevel.IsSubLevel && !thisLevel.IsSubLevelParent && thisLevel.HasLevelBelow)
                                {
                                    thisLevel.NextLevelBelow = levelsByGuidDict[levelBelowGuid];
                                    thisLevel.HeightJustThisLevel = thisLevel.ForgeLevelElevation - thisLevel.NextLevelBelow.ForgeLevelElevation;
                                    break;
                                }
                                if (!thisLevel.IsSubLevel && !thisLevel.IsSubLevelParent && !thisLevel.HasLevelBelow)
                                {
                                    thisLevel.HeightJustThisLevel = thisLevel.ForgeLevelElevation;
                                    break;
                                }
                            }
                            else
                            {
                                if (thisLevel.LevelsBelow.Count > 0)
                                {
                                    thisLevel.HeightJustThisLevel = thisLevel.ForgeLevelElevation - levelsByGuidDict[levelBelowGuid].ForgeLevelElevation;
                                }
                                else
                                {
                                    thisLevel.HeightJustThisLevel = thisLevel.ForgeLevelElevation;
                                    thisLevel.NextLevelBelow = null;
                                    break;
                                }
                            }
                        }

                        pointsThisLevel = pointsThisBuilding.Where(p => p.LevelGuid == thisLevel.LevelGuid).Select(p => p).ToList();
                        thisLevel.PointsByLevelGuid = pointsThisLevel;

                        thisLevel.BoundingBox.SetCentroidAndPoints(thisLevel.BoundingBox.MaxPoint, thisLevel.BoundingBox.MinPoint, thisLevel.ConvexHullPoints);
                        thisLevel.LevelsBelow = GetLevelsBelow(thisLevel, forgeLevels).Select(l => l.LevelGuid).ToList();

                        foreach (var pointOnThisLevel in thisLevel.PointsByLevelGuid.ToList())
                        {
                            pointOnThisLevel.Level = thisLevel;
                        }

                        thisLevel.HorizontalPoints = pointsThisLevel.Where(p => p.IsFaceHorizontal).Select(p => p).ToList();
                        thisLevel.EdgePointsRectangular = pointsThisLevel.Where(p => p.IsEdgeRectangular).Select(p => p).ToList();
                        thisLevel.EdgePointsOval = pointsThisLevel.Where(p => p.IsEdgeOval).Select(p => p).ToList();
                        thisLevel.GableRidgeCorners = pointsThisLevel.Where(p => p.IsGableRidgeCorner).Select(p => p).ToList();
                        thisLevel.GableRidgeEdges = pointsThisLevel.Where(p => p.IsGableRidgeEdge).Select(p => p).ToList();
                        thisLevel.GableSlopedEdges = pointsThisLevel.Where(p => p.IsGableRoof).Select(p => p).ToList();
                        thisLevel.GableEaveEdges = pointsThisLevel.Where(p => p.IsGableEaveEdge).Select(p => p).ToList();
                        thisLevel.GableEaveCorners = pointsThisLevel.Where(p => p.IsGableEaveCorner).Select(p => p).ToList();

                        if (thisLevel.EdgePointsRectangular.Any())
                        {
                            thisLevel.LevelShape = LevelShape.Rectangle;
                            thisLevel.IsRectangular = true;
                        }

                        if (thisLevel.EdgePointsOval.Any())
                        {
                            thisLevel.LevelShape = LevelShape.Oval;
                            thisLevel.IsOval = true;
                        }

                        if (thisLevel.GableRidgeCorners.Any() || thisLevel.GableRidgeEdges.Any())
                        {
                            thisLevel.LevelShape = LevelShape.Gable;
                            thisLevel.IsGabel = true;
                        }

                        thisLevel.Corners = pointsThisLevel.Where(p => p.IsCorner).Select(p => p).ToList();
                        SetPointLocationForThisLevel(thisLevel);

                        var analysisEdgesThisLevel = analysisEdges?.Where(kvp => (kvp.Key.Equals(thisLevel.LevelGuid))).FirstOrDefault();
                        var minimumHeightOfGable = 0.5D;
                        var gablePoint = thisLevel.PointsByLevelGuid.Where(p => p.IsGableRoof == true || p.IsGableRidgeEdge == true).ToList();
                        var hasGablePoints = gablePoint.Any();

                        if (hasGablePoints)
                        {
                            var ridgebottomPointZ = thisLevel.GableRidgeCorners.Select(p => p.BottomPoint.Z).Max();
                            var basebottomPointZ = thisLevel.GableEaveCorners.Select(p => p.BottomPoint.Z).Min();

                            if (ridgebottomPointZ - basebottomPointZ > minimumHeightOfGable)
                            {
                                thisLevel.IsGabel = true;

                                thisLevel.GabelHeight = ridgebottomPointZ - basebottomPointZ;

                                var baseCournerArray = thisLevel.GableEaveCorners.ToArray();

                                if (thisLevel.GableRidgeCorners.Count == 2)
                                {
                                    Point ridgeCorner1 = thisLevel.GableRidgeCorners[0];
                                    Point ridgeCorner2 = thisLevel.GableRidgeCorners[1];

                                    var distance = GetHypotenuse2D(ridgeCorner1, ridgeCorner2);

                                    if (distance > 0.0D)
                                    {
                                        thisLevel.GableWidth = distance;

                                        thisLevel.HeightJustThisLevel = thisLevel.GabelHeight;
                                    }
                                }
                            }
                        }

                        levels.Add(thisLevel);
                    }

                    foreach (var thisLevel in levels.ToList())
                    {
                        bool LevelIsLevel0 = thisLevel.LevelGuid == lowestLevel.LevelGuid;

                        if (thisLevel.IsRectangular)
                        {
                            foreach (var corner in thisLevel.Corners.ToList())
                            {
                                corner.IsExtendedCornerOrEdge = corner.ExtendedPoint;
                            }

                            foreach (var rectangularEdge in thisLevel.EdgePointsRectangular.ToList())
                            {
                                rectangularEdge.IsExtendedCornerOrEdge = rectangularEdge.ExtendedPoint;
                            }
                        }

                        if (thisLevel.IsOval)
                        {
                            foreach (var ovalEdge in thisLevel.EdgePointsOval.ToList())
                            {
                                ovalEdge.IsExtendedCornerOrEdge = ovalEdge.ExtendedPoint;
                            }
                        }

                        if (thisLevel.IsGabel)
                        {
                            foreach (var gableEaveCorner in thisLevel.GableEaveCorners.ToList())
                            {
                                gableEaveCorner.IsExtendedCornerOrEdge = gableEaveCorner.ExtendedPoint;
                            }

                            foreach (var gableEaveEdge in thisLevel.GableEaveEdges.ToList())
                            {
                                gableEaveEdge.IsExtendedCornerOrEdge = gableEaveEdge.ExtendedPoint;
                            }

                            foreach (var gableEaveEdge in thisLevel.GableSlopedEdges.ToList())
                            {
                                gableEaveEdge.IsExtendedCornerOrEdge = gableEaveEdge.ExtendedPoint;
                            }

                            foreach (var gableRidgeCorner in thisLevel.GableRidgeCorners.ToList())
                            {
                                gableRidgeCorner.IsExtendedCornerOrEdge = gableRidgeCorner.ExtendedPoint;
                            }

                            foreach (var gableRidgeCorner in thisLevel.GableRidgeEdges.ToList())
                            {
                                gableRidgeCorner.IsExtendedCornerOrEdge = gableRidgeCorner.ExtendedPoint;
                            }
                        }

                        List<Terminal> dynaspheresThisLevel = new List<Terminal>();

                        if (forgeLevels.Count() == 1)
                        {
                            dynaspheresThisLevel = dynasphereAirTerminals;
                        }
                        if (forgeLevels.Count() > 1)
                        {
                            dynaspheresThisLevel = dynasphereAirTerminals.Where(t => t.LevelGuid == thisLevel.LevelGuid).Select(t => t).ToList();
                        }

                        if (dynaspheresThisLevel.Count() == 0)
                        {
                            foreach (var dynasphere in dynasphereAirTerminals.ToList())
                            {
                                if (dynasphere.LevelGuid == null || dynaspheresThisLevel.Count() == 0)
                                {
                                    dynaspheresThisLevel = dynasphereAirTerminals.
                                        Where(t =>
                                        (
                                            Math.Floor(t.Bottom.Z) <= thisLevel.ElevationForKi + comperisonTolerance &&
                                            Math.Floor(t.Bottom.Z) >= thisLevel.ElevationForKi - comperisonTolerance
                                        )).Select(t => t).ToList();
                                }
                            }
                        }

                        // Collect all the points on this level that could be the POI for any dynasphere on this level:
                        var possibleTerminalPois = new List<Point>();

                        if (thisLevel.IsRectangular)
                        {
                            possibleTerminalPois.AddRange(thisLevel.EdgePointsRectangular);
                            possibleTerminalPois.AddRange(thisLevel.Corners);
                        }

                        if (thisLevel.IsHybrid)
                        {
                            possibleTerminalPois.AddRange(thisLevel.EdgePointsRectangular);
                            possibleTerminalPois.AddRange(thisLevel.EdgePointsOval);
                            possibleTerminalPois.AddRange(thisLevel.Corners);
                        }

                        if (thisLevel.IsOval) { possibleTerminalPois.AddRange(thisLevel.EdgePointsOval); }

                        if (thisLevel.IsGabel)
                        {
                            possibleTerminalPois.AddRange(thisLevel.GableEaveCorners);
                            possibleTerminalPois.AddRange(thisLevel.GableEaveEdges);
                            possibleTerminalPois.AddRange(thisLevel.GableRidgeCorners);
                            possibleTerminalPois.AddRange(thisLevel.GableRidgeEdges);
                            possibleTerminalPois.AddRange(thisLevel.GableRidgeEdges);
                        }

                        possibleTerminalPois.AddRange(thisLevel.HorizontalPoints);

                        // Set the dynasphere POI and parameters for this level
                        foreach (var dynasphere in dynaspheresThisLevel.ToList())
                        {
                            var heightAboveLevel = dynasphere.Top.Z - thisLevel.ForgeLevelElevation;
                            var thisDynasphere = dynasphere;
                            thisDynasphere.Level = thisLevel;

                            if (heightAboveLevel > 0.0)
                            {
                                thisDynasphere = SetKeyParametersForTerminal(dynasphere, thisDynasphere.Lpl, building.H_Site, heightAboveLevel);
                            }
                            else
                            {
                                thisDynasphere = SetKeyParametersForTerminal(dynasphere, thisDynasphere.Lpl, building.H_Site, 0.1);
                            }

                            var pointsCloseToTerminal = new List<Point>();
                            var cornerPointsInProximity = new List<Point>();
                            var edgePointsInProximity = new List<Point>();
                            var middlePointsInProximity = new List<Point>();

                            foreach (var possiblePoi in possibleTerminalPois.ToList())
                            {
                                if (PointIsInsideCircle(thisDynasphere.Position.X, thisDynasphere.Position.Y, possiblePoi.Position.X, possiblePoi.Position.Y, 1.50D))
                                {
                                    pointsCloseToTerminal.Add(possiblePoi);

                                    switch (thisLevel.LevelShape)
                                    {
                                        case LevelShape.Rectangle:
                                            switch (possiblePoi.LocationOnStucture)
                                            {
                                                case PoiLocation.Corner:
                                                    cornerPointsInProximity.Add(possiblePoi);
                                                    break;
                                                case PoiLocation.Edge:
                                                    edgePointsInProximity.Add(possiblePoi);
                                                    break;
                                                case PoiLocation.Middle:
                                                    middlePointsInProximity.Add(possiblePoi);
                                                    break;
                                                default:
                                                    break;
                                            }
                                            break;

                                        case LevelShape.Oval:
                                            switch (possiblePoi.LocationOnStucture)
                                            {
                                                case PoiLocation.Edge:
                                                    edgePointsInProximity.Add(possiblePoi);
                                                    break;
                                                case PoiLocation.Middle:
                                                    middlePointsInProximity.Add(possiblePoi);
                                                    break;
                                                default:
                                                    break;
                                            }
                                            break;
                                        case LevelShape.Gable:
                                            switch (possiblePoi.LocationOnStucture)
                                            {
                                                case PoiLocation.GableEaveCorner:
                                                    cornerPointsInProximity.Add(possiblePoi);
                                                    break;
                                                case PoiLocation.GableEaveEdge:
                                                    edgePointsInProximity.Add(possiblePoi);
                                                    break;
                                                case PoiLocation.GableRidgeCorner:
                                                    cornerPointsInProximity.Add(possiblePoi);
                                                    break;
                                                case PoiLocation.GableRidgeEdge:
                                                    edgePointsInProximity.Add(possiblePoi);
                                                    break;
                                                case PoiLocation.Middle:
                                                    middlePointsInProximity.Add(possiblePoi);
                                                    break;
                                                default:
                                                    break;
                                            }
                                            break;
                                        default:
                                            break;
                                    }
                                }
                            }

                            if (cornerPointsInProximity.Any())
                            {
                                var poi = cornerPointsInProximity.First();
                                thisDynasphere.PoiPoint = poi;
                                thisDynasphere.LocationOnStucture = poi.LocationOnStucture;
                                thisLevel.DynosphereAirTerminals.Add(thisDynasphere);
                            }

                            if (!cornerPointsInProximity.Any() && edgePointsInProximity.Any())
                            {
                                var poi = edgePointsInProximity.First();
                                thisDynasphere.PoiPoint = poi;
                                thisDynasphere.LocationOnStucture = poi.LocationOnStucture;
                                thisLevel.DynosphereAirTerminals.Add(thisDynasphere);
                            }

                            if (!cornerPointsInProximity.Any() && !edgePointsInProximity.Any() && pointsCloseToTerminal.Any())
                            {
                                var poi = pointsCloseToTerminal.First();
                                thisDynasphere.PoiPoint = poi;
                                thisDynasphere.LocationOnStucture = poi.LocationOnStucture;
                                thisLevel.DynosphereAirTerminals.Add(thisDynasphere);
                            }

                        }
                    }

                    building.Levels = levels;
                }
                foreach (var level in building.Levels.ToList())
                {
                    var pointsAbove = new List<Point>();

                    level.LevelsAbove = building.Levels.Where(l => l.ForgeLevelElevation > level.ForgeLevelElevation).Select(l => l.LevelGuid).ToList();

                    foreach (var levelAbove in level.LevelsAbove.ToList())
                    {
                        pointsAbove.AddRange(levelsByGuidDict[levelAbove].EdgePointsRectangular);
                        pointsAbove.AddRange(levelsByGuidDict[levelAbove].EdgePointsOval);
                        pointsAbove.AddRange(levelsByGuidDict[levelAbove].GableEaveCorners);
                        pointsAbove.AddRange(levelsByGuidDict[levelAbove].GableEaveEdges);
                        pointsAbove.AddRange(levelsByGuidDict[levelAbove].GableSlopedEdges);
                        pointsAbove.AddRange(levelsByGuidDict[levelAbove].GableRidgeCorners);
                        pointsAbove.AddRange(levelsByGuidDict[levelAbove].GableRidgeEdges);
                        pointsAbove.AddRange(levelsByGuidDict[levelAbove].Corners);
                    }
                }


            }
            catch (Exception ex)
            {
                throw ex;
            }

            return building;
        }

        /// <summary> Sets point location for this level. </summary>
        ///
        /// <exception cref="Exception"> Thrown when an exception error condition occurs. </exception>
        ///
        /// <param name="thisLevel"> this Forge level. </param>
        private static void SetPointLocationForThisLevel(Level thisLevel)
        {
            try
            {
                // Edges
                foreach (var point in thisLevel.EdgePointsOval.ToList())
                {
                    point.LocationOnStucture = PoiLocation.Edge;
                }

                foreach (var point in thisLevel.EdgePointsRectangular.ToList())
                {
                    point.LocationOnStucture = PoiLocation.Edge;
                }

                foreach (var point in thisLevel.CvmEdgePoints.ToList())
                {
                    point.LocationOnStucture = PoiLocation.Edge;
                }

                // Corners
                foreach (var point in thisLevel.Corners.ToList())
                {
                    point.LocationOnStucture = PoiLocation.Corner;
                }

                // Horizontal 
                foreach (var point in thisLevel.HorizontalPoints.ToList())
                {
                    point.LocationOnStucture = PoiLocation.Middle;
                }

                // Gable Eave Edges
                foreach (var point in thisLevel.GableEaveEdges.ToList())
                {
                    point.LocationOnStucture = PoiLocation.GableEaveEdge;
                }

                // Gable Eave Corners
                foreach (var point in thisLevel.GableEaveCorners.ToList())
                {
                    point.LocationOnStucture = PoiLocation.GableEaveCorner;
                }

                // Gable Sloped Edges
                foreach (var point in thisLevel.GableSlopedEdges.ToList())
                {
                    point.LocationOnStucture = PoiLocation.GableSlope;
                }

                // Gable Ridge Edges
                foreach (var point in thisLevel.GableRidgeEdges.ToList())
                {
                    point.LocationOnStucture = PoiLocation.GableRidgeEdge;
                }

                // Gable Ridge Corners
                foreach (var point in thisLevel.GableRidgeCorners.ToList())
                {
                    point.LocationOnStucture = PoiLocation.GableRidgeCorner;
                }
            }
            catch (Exception ex)
            {
                throw ex;
            }
        }

        /// <summary> Point is on exteded edge. </summary>
        ///
        /// <exception cref="Exception"> Thrown when an exception error condition occurs. </exception>
        ///
        /// <param name="poi"> The poi. </param>
        /// <param name="pointsBelowToCheck"> The points below to check. </param>
        private bool PointIsOnExtededEdge(Point poi, List<Point> pointsBelowToCheck)
        {
            var isOnExtended = true;
            try
            {
                foreach (var pointBelow in pointsBelowToCheck)
                {
                    if (PointIsInsideCircle(poi.Position.X, poi.Position.Y, pointBelow.Position.X, pointBelow.Position.Y, 1.75))
                    {
                        isOnExtended = false;
                    }
                }
            }
            catch (Exception ex)
            {

                throw ex;
            }

            return isOnExtended;
        }


        private List<Level> GetLevelsBelow(Level thisLevel, List<Level> forgeLevels)
        {
            var replacementList = new List<Level>();
            foreach (var levelGuid in thisLevel.LevelsBelow)
            {
                var levelBelow = forgeLevels.Where(l => l.LevelGuid == levelGuid).FirstOrDefault();
                if (levelBelow != null)
                {
                    replacementList.Add(levelBelow);
                }
            }

            return replacementList;
        }

        /// <summary> Is sub-level below this sub-level. </summary>
        ///
        /// <param name="thisLevel"> this level. </param>
        /// <param name="allLevelsBelowThisLevel"> all levels below this level. </param>
        /// <param name="levelBelow"> The level below. </param>
        private static bool IsSublevelBelowThisSublevel(Level thisLevel, List<Level> allLevelsBelowThisLevel, Level levelBelow)
        {
            var siblingSubLevles = allLevelsBelowThisLevel.Where(l => l.ParentLevelGuid == levelBelow.ParentLevelGuid).ToList();

            if (siblingSubLevles.Count > 0)
            {
                // Find the sub-level below this one:
                foreach (var subLevel in siblingSubLevles.ToList())
                {
                    // get the centroid of this level's bounding box.
                    subLevel.BoundingBox.SetCentroidAndPoints(thisLevel.BoundingBox.MaxPoint, thisLevel.BoundingBox.MinPoint, thisLevel.ConvexHullPoints);
                    subLevel.BoundingBox.SetCentroidAndPoints(levelBelow.BoundingBox.MaxPoint, levelBelow.BoundingBox.MinPoint, thisLevel.ConvexHullPoints);

                    //if (thisLevelbbPoints.Count > 3 && thisLevelBbCentroid != null & levelBelowbbPoints.Count > 3)
                    if (thisLevel.BoundingBox.BoundingBoxPoints.Count > 3 && thisLevel.BoundingBox.BoundingBoxCentroid != null
                                                                          && levelBelow.BoundingBox.BoundingBoxPoints.Count > 3)
                    {
                        var isOverThisSubLevel = threeVector3.IsPointInPolygon(levelBelow.BoundingBox.BoundingBoxPoints.ToArray(), thisLevel.BoundingBox.BoundingBoxCentroid);

                        if (isOverThisSubLevel)
                        {
                            return true;
                        }
                    }
                }
            }
            return false;
        }

        #endregion Rationalize Building's Geometry

        #region Calls to KiEngine for Dynaspheres and Points

        /// <summary> Gets ki data for dynasphere. </summary>
        ///
        /// <param name="building"> The current building. </param>
        /// <param name="baseLevelOfBuilding"> The base level of current building. </param>
        /// <param name="otherBldgs"> other buildings in the project. </param>
        /// <param name="terminal"> The terminal to evaluate. </param>
        /// <param name="site"> The building's site request data. </param>
        /// <param name="poiPoint"> The corner or edge point. </param>
        public Terminal GetKiDataForDynasphere(Building building,
                                               Level baseLevelOfBuilding,
                                               List<Building> otherBldgs,
                                               Terminal terminal,
                                               Site site,
                                               Point poiPoint)
        {
            try
            {
                List<string> calculatedFormulaLetters = GetMultiplicativeFormulas(site: site,
                                                                                  building: building,
                                                                                  baseLevelOfBuilding: baseLevelOfBuilding,
                                                                                  poiPoint: poiPoint,
                                                                                  terminal: terminal,
                                                                                  userCookie: null);
                List<Level> levelAboveOnOtherBuildings = new List<Level>();

                foreach (Building bldg in otherBldgs)
                {
                    var levelsAbove = bldg.Levels.Where(l => l.ForgeLevelElevation > terminal.PoiPoint.Level.ForgeLevelElevation).Select(l => l).ToList();
                    if (levelsAbove.Count > 0)
                    {
                        levelAboveOnOtherBuildings.AddRange(levelsAbove);
                    }
                }

                // Get all Ki data:
                var kiData = new KiEngine(calculatedFormulaLetters,
                                          site,
                                          building,
                                          baseLevelOfBuilding,
                                          levelAboveOnOtherBuildings,
                                          poiPoint,
                                          terminal,
                                          UserCookie);
                return kiData.Terminal;
            }
            catch (Exception ex)
            {
                string className = "CvmEngine";
                string methodName = "GetKiForAirForDynasphere";
                LogReport report = new LogReport(className, methodName, LogLevel.High, ex.Message, ex.StackTrace, UserCookie, new
                {
                    terminal
                });
                report.WriteReport();
            }

            return null;
        }

        /// <summary> Gets ki data for point. </summary>
        ///
        /// <param name="building"> The current building. </param>
        /// <param name="baseLevelOfBuilding"> The base level of current building. </param>
        /// <param name="otherBldgs"> other buildings in the project. </param>
        /// <param name="site"> The building's site request data. </param>
        /// <param name="poiPoint"> The current corner or edge point. </param>
        public Point GetKiDataForPoint(Building building,
                                       Level baseLevelOfBuilding,
                                       List<Building> otherBldgs,
                                       Site site,
                                       Point poiPoint)
        {
            try
            {
                List<string> calculatedFormulaLetters = GetMultiplicativeFormulas(site: site,
                                                                                  building: building,
                                                                                  baseLevelOfBuilding: baseLevelOfBuilding,
                                                                                  poiPoint: poiPoint,
                                                                                  terminal: null,
                                                                                  userCookie: null);
                List<Level> levelAboveOnOtherBuildings = new List<Level>();

                foreach (Building bldg in otherBldgs)
                {
                    var levelsAbove = bldg.Levels.Where(l => l.ForgeLevelElevation > poiPoint.Level.ForgeLevelElevation).Select(l => l).ToList();
                    if (levelsAbove.Count > 0)
                    {
                        levelAboveOnOtherBuildings.AddRange(levelsAbove);
                    }
                }

                var kiData = new KiEngine(calculatedFormulaLetters,
                                          site,
                                          building,
                                          baseLevelOfBuilding,
                                          levelAboveOnOtherBuildings,
                                          poiPoint,
                                          terminal: null,
                                          UserCookie);
                return kiData.Point;
            }
            catch (Exception ex)
            {
                string className = "CvmEngine";
                string methodName = "GetKiForAirForDynasphere";
                LogReport report = new LogReport(className, methodName, LogLevel.High, ex.Message, ex.StackTrace, UserCookie, new
                {
                    poiPoint
                });
                report.WriteReport();
            }

            return null;
        }

        #endregion Calls to KiEngine for Dynaspheres and Points

        #region CVM Methods

        /// <summary> Collection Volume Up Method. </summary>
        ///
        /// <param name="breakDownE_Field"> The break down e-field. </param>
        /// <param name="q_LeaderCharge"> The Q-leader charge. </param>
        /// <param name="cloudBase"> (Optional) The cloud base at a default elevation of 5000M . </param>
        public double CvmUp(double breakDownE_Field, double q_LeaderCharge, double cloudBase = 5000.00D)
        {
            // Returning zm : zm represents the downward leader's elevation (from a point AGL) where an upward leader is formed.
            double zm = 0;

            var tuple = Tuple.Create(breakDownE_Field, q_LeaderCharge, cloudBase);

            try
            {
                // Solving for E_b
                double E_b;

                // A value calculated from the site elevation:
                var breakdownField = breakDownE_Field;

                // Q=0.16; Charge based on LPL
                // h = 5000; Cloudbase height
                // Se = 0;  Site Elevation
                // E0 = 3.1E6; % Default breakdown E-field

                do
                {
                    // iteration precision:
                    zm += 0.01;

                    // Full formula
                    // E_B = Q / (πε(h - z)^2 )  [((h-z))/z+ln⁡(z/h) ]

                    //(πε(h - z) ^ 2
                    var denominator = (Math.PI * ElectricalEpsilon) * (Math.Pow((cloudBase - zm), 2));

                    // E_B = Q / (πε(h - z)^2 )
                    var firstEval = q_LeaderCharge / denominator;

                    // ln⁡(z/h)
                    var logValue = Math.Log(zm / cloudBase);

                    // [((h -z))/ z + ln⁡(z/h) ]
                    var secondEval = ((cloudBase - zm) / zm) + logValue;

                    // Solve for E_b
                    E_b = firstEval * secondEval;

                } while (E_b > breakdownField && (cloudBase - zm) >= 0);

                // Correct for first iteration which evaluates to be NaN
                zm -= 0.01;

                //var exception = new Exception("Text Exception");
                //throw exception;

                return zm;
            }
            catch (Exception ex)
            {
                string className = "CvmEngine";
                string methodName = "CvmUp";
                LogReport report = new LogReport(className, methodName, LogLevel.High, ex.Message, ex.StackTrace, UserCookie, new
                {
                    tuple
                });
                report.WriteReport();
            }

            return zm;
        }

        /// <summary> Collection Volume Method Down. </summary>
        ///
        /// <param name="kiTotalContribution"> The ki total contribution. </param>
        /// <param name="breakDownE_Field"> The break down e field. </param>
        /// <param name="q_LeaderCharge"> The leader charge. </param>
        /// <param name="cloudBase"> (Optional) The cloud base. </param>
        public double CvmDown(double kiTotalContribution, double breakDownE_Field, double q_LeaderCharge, double cloudBase = 5000.00D)
        {
            // d_s is the striking distance or the height above an air terminal that the downward leader is when an upward leader is formed
            double d_s = 0.0;

            var tuple = Tuple.Create(kiTotalContribution, breakDownE_Field, q_LeaderCharge, cloudBase);

            try
            {
                var Ki = 50.0D;
                var building = Buildings.FirstOrDefault();
                if (building != null)
                {
                    Ki = kiTotalContribution;
                }

                // Collection Volume Down
                double E_A;

                // d is a constant representing the horizontal step distance of 0.5m aka 500cm
                double d = 0.5D;

                double e_upleader = breakDownE_Field / Ki;

                double z = 0.0;

                do
                {
                    // Full equation:
                    // E_A = Q/(〖πεd〗^2 (h/d- z/d)^2 )  [ ((h/d - z/d))/{1 + (z/d)^2 } + sinh^(-1)⁡(z/d) - sinh^(-1)⁡(h/d) ]

                    // EA1 = (Q / (pi * Ep * (h - z)^2));
                    double eval1 = q_LeaderCharge / (Math.PI * ElectricalEpsilon * (Math.Pow(cloudBase - z, 2)));

                    // EA2 = (h/d - z/d) / ((1 + (z/d)^2)^0.5)
                    double eval2 = ((cloudBase / d) - (z / d)) / Math.Pow((1 + System.Math.Pow(z / d, 2)), 0.5);

                    // EA = Eval_1 [Eval_2 + sinh^(-1)⁡ (z/d) - sinh^(-1)⁡ (h/d)]
                    E_A = eval1 * (eval2 + Math.Asinh(z / d) - Math.Asinh(cloudBase / d));

                    // correct for first result which resulted NaN
                    d_s = Math.Round(z, 4) - 0.01;

                    z += 0.01;
                }
                while (E_A > e_upleader && z <= cloudBase);

                // result is 0 if there is no leader interception
                return d_s;
            }
            catch (Exception ex)
            {
                string className = "CvmEngine";
                string methodName = "CvmDown";
                LogReport report = new LogReport(className, methodName, LogLevel.High, ex.Message, ex.StackTrace, UserCookie, new
                {
                    tuple
                });
                report.WriteReport();
            }

            return d_s;
        }

        /// <summary> Gets attractive radius and its height above the POI. </summary>
        ///
        /// <param name="z_m"> From CVM UP: z_m: represents the downward leader’s elevation from a point on the ground (AGL),
        ///                    when an upward leader is formed. </param>
        /// <param name="d_s"> From CVM Down: d_s is the striking distance or the height above an air terminal that the
        ///                    downward leader is when an upward leader is formed. </param>
        /// <param name="poiHeight"> The height of the POI AGL above ground level. Typically the Top Z of the dynasphere. </param>
        /// <param name="forTerminal"> (Optional) True if the POI is a dynasphere air terminal. </param>
        public VelocityDerivedBoundary GetAttractiveRadius(double z_m, double d_s, double poiHeight, Terminal terminal = null)
        {
            // a struct containing all the required attractive radius data;
            var vdbData = new VelocityDerivedBoundary();

            try
            {
                double z_max = 0.0;

                // Solve for:
                // R_a which is the protection radius defined by the intersection of the two curves
                // Z_r which is the height of the intersection of the two curves above z = 0; 
                // Z_at which is the height of the intersection of the air terminal tip;

                // Givens:
                // 	z_m, output from CVM Up
                //  K_V, velocity ratio this is a constant
                double K_v = terminal == null ? 1.1D : terminal.VelocityRatioKv;
                //  H, height of air terminal tip above the POI
                // var H = poiHeight;
                var H = terminal.Top.Z;
                var y_max = 2 * H;
                //  d_s, striking distance from CVM Down


                // Assumptions
                // 	d_s ≥ (z_m (K_v - 1) + H)/K_v ,else R_a = d_s

                // Curve one - the velocity driven boundary
                //  d_z(z) = √(〖((z_m (K_v-1)+z)/K_v )〗^2-〖(z - H)〗^2 )
                //  
                //  Curve two - the striking distance curve
                //  d(z) = √(d_s^2 -〖(z - H)〗^2 )


                // z_r is the z-component at which the two formulas intersect  d = d_z
                // 
                // z_r = K_v d_s - z_m(K_v - 1)
                // 
                // Z_at = (Z_r - H)
                // 
                // R_a =√(d_s^2 -〖(z_r - H)〗^2 )

                //var z_0 = (K_v * H - z_m * (K_v - 1)) / (K_v + 1); // minimum x point below which the velocity-derived boundary is truncated
                var z_0 = Math.Round((K_v * H - z_m * (K_v - 1)) / (K_v + 1) + 0.01, 2); //  minimum x point below which the velocity-derived boundary is truncated 4-6-2021

                //if (d_s < z_0)
                //{
                //    R_a = d_s;
                //    z_r = H;
                //    y_max = 2 * H;
                //}
                if (d_s < z_0)
                {
                    vdbData.AttractiveRadius = d_s;

                    // Z_r is the total elevation from ground level to the attractive radius.
                    // It is also the elevation (at which) the VDB and the dome of protection intersect
                    vdbData.Z_r = H;
                    z_max = 2 * H;
                }
                //else if (d_s > 5 * H)
                //{
                //    // Ra=sqrt(((zm*(Kv-1)+(5*H))/Kv)^2-(4*H)^2);
                //    R_a = Math.Sqrt((Math.Pow(((z_m * (K_v - 1) + (5 * H)) / K_v), 2) - Math.Pow((4 * H), 2)));
                //    z_r = 5 * H;
                //}
                else if (d_s > 5 * H)
                {
                    vdbData.AttractiveRadius = Math.Sqrt((Math.Pow(((z_m * (K_v - 1) + (5 * H)) / K_v), 2) - Math.Pow((4 * H), 2))); // attractive radius
                    vdbData.Z_r = 5 * H; // Zr is the elevation (at which) the VDB and the dome of protection intersect
                }
                //else
                //{
                //    z_r = K_v * d_s - z_m * (K_v - 1); // height of intersection of the velocity derived boundary and the dome of protection intersect
                //    R_a = Math.Sqrt(Math.Pow(d_s, 2) - Math.Pow((z_r - H), 2)); // attractive radius
                //}
                else
                {
                    //z_r = K_v * d_s - z_m * (K_v - 1); // Zr is the elevation (at which) the VDB and the dome of protection intersect

                    vdbData.Z_r = K_v * d_s - z_m * (K_v - 1);

                    if (vdbData.Z_r < H)
                    {
                        vdbData.Z_r = H;
                    }

                    // R_a = sqrt(d_s^2 - (z_r-H)^2);  attractive radius R_a
                    vdbData.AttractiveRadius = Math.Sqrt(Math.Pow(d_s, 2) - Math.Pow((vdbData.Z_r - H), 2)); // attractive radius
                }

                return vdbData;
            }
            catch (Exception ex)
            {
                string className = "CvmEngine";
                string methodName = "GetAttractiveRadius";
                LogReport report = new LogReport(className, methodName, LogLevel.High, ex.Message, ex.StackTrace, UserCookie, new
                {
                    vdbData
                });
                report.WriteReport();
            }

            return vdbData;
        }

        /// <summary> Velocity boundary range points. </summary>
        ///
        /// <param name="zm"> The zm derived from the CvmUp Method.
        ///                       zm represents the downward leader's elevation (from a point AGL) where an upward leader
        ///                       is formed. </param>
        /// <param name="terminal"> The dynasphere air terminal. </param>
        /// <param name="vdbData"> The data describing the velocity derived boundary. </param>
        public VelocityDerivedBoundary GetVelocityBoundaryPoints(double zm, Terminal terminal, VelocityDerivedBoundary vdbData)
        {
            var vdbPoints = new List<Point>();
            var dictionary = new Dictionary<double, double>();

            try
            {
                double K_v = terminal == null ? 1.1D : terminal.VelocityRatioKv;

                var H = terminal.Top.Z;;

                var z = H;

                var rangeCeiling = H * 5;

                var zIterator = 0.01D;

                var d = 00.0D;

                // collect the value ranges for d and z:
                do
                {
                    // d = √(〖((z_m (K_v-1)+z)/K_v )〗^2-〖(z-H)〗^2 )
                    var eval1 = Math.Pow(zm * (K_v - 1) + z / K_v, 2);
                    var eval2 = Math.Pow(z - H, 2);

                    var eval3 = eval1 - eval2;
                    d = Math.Sqrt(eval1 - eval2);

                    dictionary.Add(d, z);

                    z += zIterator;

                } while (z < rangeCeiling);

                // Get 6 points along the velocity derived boundary curve:
                var z1 = terminal.Top.Z;
                var z6 = vdbData.Z_r;

                var dmin = dictionary.Keys.Min();
                // the first point's d value (the closes Y value from the air terminal
                var d1 = dictionary.Where(d => d.Key == dmin).Select(kvp => kvp.Key).FirstOrDefault();

                // the last point's d value
                var d6 = vdbData.AttractiveRadius;

                if (d6 > d1)
                {
                    // d-step values along the y-axis
                    var dStep = (d6 - d1) / 5;

                    // The first point at the height (terminal top z value) of the air terminal
                    var firstPoint = new VelocityBoundaryPoint()
                    {
                        X = terminal.Top.X,
                        Y = terminal.Top.Y + d1,
                        Z = terminal.Top.Z
                    };
                    // add the first point
                    vdbData.VDB_Points.Add(firstPoint);

                    var dx = d1 + dStep;

                    // Collect four middle points
                    for (int i = 0; i < 4; i++)
                    {
                        // Get the point for this d-step
                        var boundaryValues = dictionary.Where(kvp => kvp.Key < dx + 0.01 && kvp.Key > dx - 0.01).FirstOrDefault();

                        var point = new VelocityBoundaryPoint()
                        {
                            X = terminal.Top.X, // all X values are the same (we are facing the Y axis)
                            Y = terminal.Top.Y + boundaryValues.Key,
                            Z = terminal.Top.Z + boundaryValues.Value - z1
                        };

                        // add the point for this d-step
                        vdbData.VDB_Points.Add(point);

                        dx += dStep;
                    }

                    // The last point at the attractive radius point
                    var lastPoint = new VelocityBoundaryPoint()
                    {
                        X = terminal.Top.X,
                        Y = terminal.Top.Y + d6,
                        Z = terminal.Top.Z + z6 - z1
                    };
                    // add the last point
                    vdbData.VDB_Points.Add(lastPoint);

                    //if (true) // if imperial measurements
                    //{
                    //    foreach (var point in vdbData.VDB_Points.ToList())
                    //    {
                    //        point.X *= 0.3048;
                    //        point.Y *= 0.3048;
                    //        point.Z *= 0.3048;
                    //    }
                    //}
                }
            }
            catch (Exception ex)
            {
                string className = "CvmEngine";
                string methodName = "VelocityBoundaryRanges";
                LogReport report = new LogReport(className, methodName, LogLevel.High, ex.Message, ex.StackTrace, UserCookie, new
                {
                    terminal
                });
                report.WriteReport();
            }

            return vdbData;
        }

        #endregion CVM Methods

        #region Helper Methods

        /// <summary> set the charge initially based on the protection level. </summary>
        ///
        /// <param name="terminal"> The terminal. </param>
        /// <param name="levelStr"> The level string. </param>
        /// <param name="siteElevation"> The elevation of terminal. </param>
        /// <param name="terminalHeightAboveLevel"> The height the terminal is above the level's elevation. </param>
        public Terminal SetKeyParametersForTerminal(Terminal terminal, string levelStr, double siteElevation, double terminalHeightAboveLevel)
        {
            try
            {
                terminal.HeightAboveStructure = terminalHeightAboveLevel;
                terminal.H_Site = siteElevation;

                int level = 0;

                switch (levelStr)
                {
                    case "i":
                        level = 1;
                        break;
                    case "ii":
                        level = 2;
                        break;
                    case "iii":
                        level = 3;
                        break;
                    case "iv":
                        level = 4;
                        break;
                    default:
                        break;
                }

                terminal.LevelOfProtection = level;

                double[] newCVMCharges = new double[] { 0.16, 0.38, 0.93, 1.8 };
                double[] newPeakCurrent = new double[] { 2.9, 5.4, 10.1, 15.7 };
                int[] newStrikingDistance = new int[] { 20, 30, 45, 60 };
                int[] newStrikePercentage = new int[] { 99, 97, 91, 84 };
                int[] deRatingAngles = new int[] { 26, 23, 20, 15 };
                double[] velocityRatioKv = new double[] { 1.1, 1.1, 1.075, 1.05 };

                if (terminal.Top.Z > 60.00)
                {
                    terminal.DeRatingAngle = deRatingAngles[level - 1];
                }
                else
                {
                    terminal.DeRatingAngle = 0;
                }

                if (level > 0)
                {
                    terminal.Q_LeaderCharge = newCVMCharges[level - 1];
                    terminal.PeakCurrent = newPeakCurrent[level - 1];
                    terminal.StrikingDistance = newStrikingDistance[level - 1];
                    terminal.StrikingDistancePercentage = newStrikePercentage[level - 1];
                    terminal.VelocityRatioKv = velocityRatioKv[level - 1];

                    return terminal;
                }

                return null;
            }
            catch (System.Exception ex)
            {
                string className = "CvmEngine";
                string methodName = "SetKeyParametersForTerminal";
                LogReport report = new LogReport(className, methodName, LogLevel.High, ex.Message, ex.StackTrace, UserCookie, new
                {
                    terminal
                });
                report.WriteReport();
            }

            return null;
        }

        /// <summary> Gets the hypotenuse of two 3D points. </summary>
        ///
        /// <param name="poiPoint"> The poi point. </param>
        /// <param name="pointBelow"> The point below. </param>
        internal double GetHypotenuse2D(Point poiPoint, Point pointBelow)
        {
            double lengthxyz = 0.00D;
            try
            {
                double x1 = poiPoint.Position.X;
                double y1 = poiPoint.Position.Y;
                double x2 = pointBelow.Position.X;
                double y2 = pointBelow.Position.Y;

                lengthxyz = Math.Sqrt(Math.Pow(x2 - x1, 2) + Math.Pow(y2 - y1, 2));

            }
            catch (Exception ex)
            {
                string className = "CvmEngine";
                string methodName = "GetHypotenuse2D";
                LogReport report = new LogReport(className, methodName, LogLevel.High, ex.Message, ex.StackTrace, UserCookie, new
                {
                    poiPoint
                });
                report.WriteReport();
            }

            return lengthxyz;
        }

        /// <summary> Gets the hypotenuse from point to points. </summary>
        ///
        /// <remarks> Ron, 4/15/2021. </remarks>
        ///
        /// <param name="referencePosition"> The terminal location. </param>
        /// <param name="pointPosition"> The point to evaluate. </param>
        ///
        /// <returns> Length. </returns>
        internal double GetHypotenuse3DFromPoint(Position referencePosition, Position2 pointPosition)
        {
            double lengthxyz = 0.0D;
            try
            {
                double x1 = referencePosition.X;
                double y1 = referencePosition.Y;
                double z1 = referencePosition.Z;
                double x2 = pointPosition.X;
                double y2 = pointPosition.Y;
                double z2 = pointPosition.Z;

                lengthxyz = Math.Sqrt(Math.Pow(x2 - x1, 2) + Math.Pow(y2 - y1, 2) + Math.Pow(z2 - z1, 2));

            }
            catch (Exception ex)
            {
                string className = "CvmEngine";
                string methodName = "GetHypotenuse3DFromPoint";
                LogReport report = new LogReport(className, methodName, LogLevel.High, ex.Message, ex.StackTrace, UserCookie);
                report.WriteReport();
            }
            return lengthxyz;
        }

        /// <summary> Point is inside circle. </summary>
        ///
        /// <param name="circle_X"> The circle x coordinate. </param>
        /// <param name="circle_Y"> The circle y coordinate. </param>
        /// <param name="point_X"> The point x coordinate. </param>
        /// <param name="point_Y"> The point y coordinate. </param>
        /// <param name="radius"> (Optional) The radius. </param>
        private bool PointIsInsideCircle(double circle_X, double circle_Y, double point_X, double point_Y, double radius = 3.00D)
        {
            var tuple = Tuple.Create(circle_X, circle_Y, point_X, point_Y);

            try
            {
                if ((point_X - circle_X) * (point_X - circle_X) +
                (point_Y - circle_Y) * (point_Y - circle_Y) <= radius * radius)
                {
                    return true;
                }
                else
                {
                    return false;
                }
            }
            catch (Exception ex)
            {
                string className = "CvmEngine";
                string methodName = "PointIsInsideCircle";
                LogReport report = new LogReport(className, methodName, LogLevel.High, ex.Message, ex.StackTrace, UserCookie, new
                {
                    tuple
                });
                report.WriteReport();
            }

            return false;
        }

        /// <summary> Method determines if two doubles are roughly equivalent. </summary>
        ///
        /// <exception cref="Exception"> Thrown when an exception error condition occurs. </exception>
        ///
        /// <param name="d1"> first double value. </param>
        /// <param name="d2"> second double value. </param>
        /// <param name="epsilon"> (Optional) the tolerance factor. </param>
        ///
        /// <returns> Returns true if equivalent, otherwise false. </returns>
        public bool ApproximatelyEqualDoubles(double d1, double d2, double epsilon = 0.1255D)
        {
            var tuple = Tuple.Create(d1, d2);
            try
            {
                return Math.Abs(d1 - d2) < epsilon;
            }
            catch (Exception ex)
            {
                string className = "CvmEngine";
                string methodName = "ApproximatelyEqualDoubles";
                LogReport report = new LogReport(className, methodName, LogLevel.High, ex.Message, ex.StackTrace, UserCookie, new
                {
                    tuple
                });
                report.WriteReport();
            }

            return false;
        }

        /// <summary> Sets point location lowest level. </summary>
        ///
        /// <param name="lowestLevel"> The lowest level on the Building. </param>
        /// <param name="p"> The point to evaluate. </param>
        public double PointDistanceFromBoundingBox(Level lowestLevel, Point p)
        {
            var bb = lowestLevel.BoundingBox;

            lowestLevel.BoundingBox.SetCentroidAndPoints(lowestLevel.BoundingBox.MaxPoint, lowestLevel.BoundingBox.MinPoint, lowestLevel.ConvexHullPoints);

            // outside
            var dxo = Math.Max(bb.MinPoint.x - p.Position.X, p.Position.X - bb.MaxPoint.x);
            var dyo = Math.Max(bb.MinPoint.y - p.Position.Y, p.Position.Y - bb.MaxPoint.y);
            var hypothenuse = Math.Sqrt(dxo * dxo + dyo * dyo);

            // inside
            var dxi = Math.Max(bb.MaxPoint.x - p.Position.X, p.Position.X - bb.MinPoint.x);
            var dyi = Math.Max(bb.MaxPoint.y - p.Position.Y, p.Position.Y - bb.MinPoint.y);

            return hypothenuse > 0 ? hypothenuse : Math.Min(dxi, dyi);
        }

        /// <summary> Sets point location next level down. </summary>
        ///
        /// <param name="levelBelow"> The level below. </param>
        /// <param name="referencePoint"> The corner or edge point. </param>
        private PoiLocation SetPointLocationOnNextLevelDown(Level levelBelow, Point referencePoint)
        {
            PoiLocation poiLocation = PoiLocation.None;

            try
            {
                // Begin getting the closes point to the referencePoint:
                var pointsWithinRange = new List<Point>();
                var pointsElevationRange = new List<double>();
                var pointsToCheck = new List<Point>();

                if (levelBelow.IsRectangular) { pointsToCheck.AddRange(levelBelow.EdgePointsRectangular); }
                if (levelBelow.IsOval) { pointsToCheck.AddRange(levelBelow.EdgePointsOval); }
                if (levelBelow.IsGabel)
                {
                    pointsToCheck.AddRange(levelBelow.GableRidgeEdges);
                    pointsToCheck.AddRange(levelBelow.GableEaveEdges);
                }
                pointsToCheck.AddRange(levelBelow.Corners);
                pointsToCheck.AddRange(levelBelow.HorizontalPoints);


                foreach (var pointBelow in pointsToCheck)
                {
                    var pointIsWithinRange = PointIsInsideCircle(referencePoint.Position.X, referencePoint.Position.Y,
                                                                 pointBelow.Position.X, pointBelow.Position.Y, 1.5D);
                    if (pointIsWithinRange)
                    {
                        pointsElevationRange.Add(pointBelow.Position.Z);
                        pointsWithinRange.Add(pointBelow);
                    }
                }

                if (pointsWithinRange.Count == 0)
                {
                    referencePoint.IsExtendedCornerOrEdge = false;

                }
                if (pointsWithinRange.Count > 0)
                {
                    referencePoint.IsExtendedCornerOrEdge = true;
                }

                // Get the location of the nearest point type below
                var pointToCheck = new Position();
                pointToCheck.X = referencePoint.BottomPoint.X;
                pointToCheck.Y = referencePoint.BottomPoint.Y;
                pointToCheck.Z = levelBelow.ForgeLevelElevation;

                var pointDictionary = GetClosestPointsToTerminalByType(pointToCheck, pointsWithinRange);

                if (pointDictionary != null && pointDictionary.Count >= 1)
                {
                    var dictionariesToCheck = pointDictionary.Where(pd => pd.Key < 1.75D).ToDictionary(pd => pd.Key, pd => pd.Value);
                    // Third Priority Type
                    if (pointDictionary.Where(p => p.Value.IsFaceHorizontal).Any())
                    {
                        poiLocation = PoiLocation.Middle;
                    }
                    // Second Priority Type
                    if (pointDictionary.Where(p => p.Value.IsEdgeRectangular || p.Value.IsEdgeOval || p.Value.IsGableRoof).Any())
                    {
                        poiLocation = PoiLocation.Edge;
                    }
                    // First Priority Type
                    if (pointDictionary.Where(p => p.Value.IsCorner).Any())
                    {
                        poiLocation = PoiLocation.Corner;
                    }
                    var closestDistance = pointDictionary.Select(p => p.Key).Min();
                    var point = pointDictionary.Where(pd => pd.Key == closestDistance).Select(pd => pd.Value).FirstOrDefault();
                    //if (point != null)
                    //{
                    //    if (point.IsCorner) { point.LocationOnStucture = PoiLocation.Corner; }
                    //    if (point.IsEdgeRectangular || point.IsEdgeOval || point.IsGableRoof) { point.LocationOnStucture = PoiLocation.Edge; }
                    //    if (point.IsFaceHorizontal) { point.LocationOnStucture = PoiLocation.Middle; }

                    //}
                }
            }
            catch (Exception ex)
            {
                string className = "CvmEngine";
                string methodName = "SetPointLocationOnNextLevelDown";
                LogReport report = new LogReport(className, methodName, LogLevel.High, ex.Message, ex.StackTrace, UserCookie, poiLocation);
                report.WriteReport();
            }

            return poiLocation;
        }

        /// <summary> Points are collinear. </summary>
        ///
        /// <param name="pArray"> The array. </param>
        /// <param name="isGabel"> (Optional) True if is gabel, false if not. </param>
        public bool PointsAreCollinear(BottomPoint[] pArray, bool isGabel = false)
        {
            double result = -1;

            try
            {
                if (!isGabel)
                {
                    var x1 = pArray[0].X;
                    var x2 = pArray[1].X;
                    var x3 = pArray[2].X;
                    var y1 = pArray[0].Y;
                    var y2 = pArray[1].Y;
                    var y3 = pArray[2].Y;

                    // Horizontally Collinear
                    // Area of a triangle
                    // 0.5 * [x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)]
                    result = 0.5 * (x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2));

                    ApproximatelyEqualDoubles(result, 0D);
                }
                if (ApproximatelyEqualDoubles(result, 0)) { return true; }
                else { return false; }
            }
            catch (Exception ex)
            {
                string className = "CvmEngine";
                string methodName = "PointsAreCollinear";
                LogReport report = new LogReport(className, methodName, LogLevel.High, ex.Message, ex.StackTrace, UserCookie, new
                {
                    pArray
                });
                report.WriteReport();
                return false;
            }
        }

        /// <summary> Gets the points closest by type to the terminal bottom being evaluated. </summary>
        ///
        /// <remarks> Carlo, 3/27/2021. </remarks>
        ///
        /// <param name="referencePosition"> The reference position to calculated the distance from. </param>
        /// <param name="points"> The points to compare to the terminal bottom. </param>
        /// <param name="userCookie"> (Optional) The user cookie. </param>
        ///
        /// <returns> The point closest to the terminal bottom. </returns>
        internal Dictionary<double, Point> GetClosestPointsToTerminalByType(Position referencePosition, IList<Point> points, dynamic userCookie = null)
        {
            Dictionary<double, Point> returnData = new Dictionary<double, Point>();
            try
            {
                double distCorner = 5000;
                double distEdge = 5000;
                double distHorizontal = 5000;

                Point closestCorner = null;
                Point closestEdge = null;
                Point closestHorizontal = null;

                //Only evaluate a list with points
                if (points.Count > 0)
                {
                    //Otherwise cycle through the points
                    foreach (Point point in points)
                    {
                        //If the closestCorner is null, the first corner point will be the closest
                        if (closestCorner == null && point.IsCorner)
                        {
                            closestCorner = point;
                            GetDistanceBetwee3DPoints(referencePosition, ref distCorner, ref closestCorner, point);
                        }
                        else if (point.IsCorner)
                        {
                            GetDistanceBetwee3DPoints(referencePosition, ref distCorner, ref closestCorner, point);
                        }

                        //If the closestEdge is null, the first edge point will be the closest
                        if (closestEdge == null && (point.IsEdgeOval || point.IsEdgeRectangular))
                        {
                            closestEdge = point;
                            GetDistanceBetwee3DPoints(referencePosition, ref distEdge, ref closestEdge, point);
                        }
                        else if (point.IsEdgeOval || point.IsEdgeRectangular)
                        {
                            GetDistanceBetwee3DPoints(referencePosition, ref distEdge, ref closestEdge, point);
                        }

                        //If the closestHorizontal is null, the first horizontal point will be the closest
                        if (closestHorizontal == null && point.IsFaceHorizontal)
                        {
                            closestHorizontal = point;
                            GetDistanceBetwee3DPoints(referencePosition, ref distHorizontal, ref closestHorizontal, point);
                        }
                        else if (point.IsFaceHorizontal)
                        {
                            GetDistanceBetwee3DPoints(referencePosition, ref distHorizontal, ref closestHorizontal, point);
                        }
                    }

                    if (closestCorner != null) { returnData.Add(distCorner, closestCorner); }
                    if (closestEdge != null) { returnData.Add(distEdge, closestEdge); }
                    if (closestHorizontal != null) { returnData.Add(distHorizontal, closestHorizontal); }

                    //Return the closest point
                    return returnData;
                }
                else
                {
                    //Return null if the list is empty
                    return null;
                }
            }
            catch (Exception ex)
            {
                string className = "CvmEngine";
                string methodName = "GetClosestPointsToTerminalByType";
                LogReport report = new LogReport(className, methodName, LogLevel.High, ex.Message, ex.StackTrace, userCookie, new { referencePosition, points });
                report.WriteReport();
                return null;
            }
        }

        /// <summary> Gets distance betwee 3D points. </summary>
        ///
        /// <param name="referencePosition"> The terminal location. </param>
        /// <param name="distHorizontal"> [in,out] The distance horizontal. </param>
        /// <param name="closestHorizontal"> [in,out] The closest horizontal. </param>
        /// <param name="point"> The corner or edge point. </param>
        internal void GetDistanceBetwee3DPoints(Position referencePosition, ref double distHorizontal, ref Point closestHorizontal, Point point)
        {
            try
            {
                //Compare the distance between the comparison point and the current point.
                var dist1 = GetHypotenuse3DFromPoint(referencePosition, point.Position);
                if (dist1 < distHorizontal)
                {
                    //If the distance is less than the current shortest distance, it is the new shortest distance;
                    distHorizontal = dist1;
                    //The point being evaluated is now the closest point.
                    closestHorizontal = point;
                }
            }
            catch (Exception ex)
            {
                string className = "CvmEngine";
                string methodName = "GetClosestPointsToTerminalByType";
                LogReport report = new LogReport(className, methodName, LogLevel.High, ex.Message, ex.StackTrace, UserCookie, new { distHorizontal, referencePosition, point });
                report.WriteReport();
            }
        }

        #endregion Helper Methods
    }
}