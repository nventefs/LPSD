// Copyright (c) 2022 Applied Software Technology, Inc.

using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Numerics;

namespace nVentErico.LPSD.Controllers.Cvm
{
    #region CVM JSON Data

    public class Building
    {
        [JsonProperty("fileName")]
        public string FileName { get; set; }

        [JsonProperty("name")]
        public string Name { get; set; }

        [JsonProperty("guid")]
        public string Guid { get; set; }

        [JsonProperty("isSubBuilding")]
        public bool IsSubBuilding;

        /// <summary> Gets or sets the site elevation in meters. 
        ///           The default value is 0.0 meters</summary>
        [JsonIgnore]
        public double H_Site { get; set; } = 0.0D;

        /// <summary> The backing-field member for the break down e-field property. </summary>
        [JsonIgnore]
        private double breakDownE_Field = 3100000D;

        /// <summary> Gets the break down e field. </summary>
        [JsonIgnore]
        public double BreakDownE_Field
        {
            get
            {
                if (H_Site > 0.0)
                {
                    breakDownE_Field *= (0.82 + 0.18 * (1 - 0.5 * (H_Site / 1000)));
                    return breakDownE_Field;
                }
                else
                {
                    return breakDownE_Field;
                }
            }
        }

        /// <summary> Gets or sets the levels. </summary>
        [JsonIgnore]
        public List<Level> Levels { get; set; }

        /// <summary> Gets or sets the lowest level of the building. </summary>
        [JsonIgnore]
        public Level BaseLevel { get; set; }

        /// <summary> Default constructor. </summary>
        public Building()
        {
            Levels = new List<Level>();
        }
    }

    public class BottomPoint
    {
        [JsonProperty("x")]
        public double X { get; set; }

        [JsonProperty("y")]
        public double Y { get; set; }

        [JsonProperty("z")]
        public double Z { get; set; }

        public BottomPoint(double x, double y, double z)
        {
            X = x;
            Y = y;
            Z = z;
        }


        public override bool Equals(object obj)
        {
            // Perform an equality check on two rectangles (Point object pairs).
            if (obj == null || GetType() != obj.GetType())
                return false;
            BottomPoint objectToCompare = (BottomPoint)obj;
            return X.Equals(objectToCompare.X) && Y.Equals(objectToCompare.Y) && Z.Equals(objectToCompare.Z);
        }

        public override int GetHashCode()
        {
            return Tuple.Create(X, Y, Z).GetHashCode();
        }
    }

    public class FaceNormal
    {
        [JsonProperty("x")]
        public double X { get; set; }

        [JsonProperty("y")]
        public double Y { get; set; }

        [JsonProperty("z")]
        public double Z { get; set; }

        public override bool Equals(object obj)
        {
            // Perform an equality check on two rectangles (Point object pairs).
            if (obj == null || GetType() != obj.GetType())
                return false;
            FaceNormal objectToCompare = (FaceNormal)obj;
            return X.Equals(objectToCompare.X) && Y.Equals(objectToCompare.Y) && Z.Equals(objectToCompare.Z);
        }

        public override int GetHashCode()
        {
            return Tuple.Create(X, Y, Z).GetHashCode();
        }
    }

    public class Site
    {
        [JsonProperty("siteElevation")]
        public string SiteElevation { get; set; }
    }

    public class SurfaceNormal
    {
        [JsonProperty("x")]
        public double X { get; set; }

        [JsonProperty("y")]
        public double Y { get; set; }

        [JsonProperty("z")]
        public double Z { get; set; }

        public override bool Equals(object obj)
        {
            // Perform an equality check on two rectangles (Point object pairs).
            if (obj == null || GetType() != obj.GetType())
                return false;
            SurfaceNormal objectToCompare = (SurfaceNormal)obj;
            return X.Equals(objectToCompare.X) && Y.Equals(objectToCompare.Y) && Z.Equals(objectToCompare.Z);
        }

        public override int GetHashCode()
        {
            return Tuple.Create(X, Y, Z).GetHashCode();
        }
    }

    /// <summary> The return results for each terminal. Gets assigned to CVMTerminalData.results properties </summary>
    /// 
    public class Terminal
    {
        [JsonProperty("bottom")]
        public Position Bottom { get; set; }

        [JsonProperty("componentType")]
        public string ComponentType { get; set; }

        [JsonProperty("hostDesignModelGuid")]
        public string HostDesignModelGuid { get; set; }

        [JsonProperty("hostDesignModelName")]
        public string HostDesignModelName { get; set; }

        [JsonProperty("levelGuid")]
        public string LevelGuid { get; set; }

        [JsonProperty("lpl")]
        public string Lpl { get; set; }

        [JsonProperty("method")]
        public string Method { get; set; }

        [JsonProperty("option")]
        public string Option { get; set; }

        [JsonProperty("position")]
        public Position Position { get; set; }

        [JsonProperty("surfaceNormal")]
        public SurfaceNormal SurfaceNormal { get; set; }

        [JsonProperty("terminalGuid")]
        public string TerminalGuid { get; set; }

        [JsonProperty("top")]
        public Top Top { get; set; }

        [JsonProperty("kiTotalContribution")]
        public double KiTotalContribution { get; set; }

        [JsonProperty("kiTotalMultiplicative")]
        public double TotalMultiplicative { get; set; }

        [JsonProperty("kiTotalReductive")]
        public double TotalReductive { get; set; }

        [JsonProperty("strikingDistance")]
        public double StrikingDistance { get; set; }

        [JsonProperty("attractiveRadius")]
        public double AttractiveRadius { get; set; }

        [JsonProperty("heightOfAttractiveRadius")]
        public double HeightOfAttractiveRadius { get; set; }

        [JsonProperty("deRatingAngle")]
        public double DeRatingAngle { get; set; }

        [JsonProperty("velocityBoundaryPoints")]
        public List<VelocityBoundaryPoint> VelocityBoundaryPoints { get; set; } = new List<VelocityBoundaryPoint>();

        [JsonIgnore]
        public Building Building { get; set; }

        [JsonIgnore]
        public Level Level { get; set; }

        [JsonProperty("poiPoint")]
        public Point PoiPoint { get; set; }

        [JsonProperty("kiData")]
        public KiDto KiData { get; set; }

        [JsonIgnore]
        public double HeightAboveStructure { get; set; }

        [JsonIgnore]
        public PoiLocation LocationOnStucture { get; set; }

        [JsonIgnore]
        public int LevelOfProtection { get; set; }

        /// <summary> Gets or sets the velocity ratio K_v. </summary>
        [JsonProperty("velocityRatioKv")]
        public double VelocityRatioKv { get; set; } = 1.10D;

        [JsonProperty("qLeaderCharge")]
        public double Q_LeaderCharge { get; set; }

        [JsonIgnore]
        public double H_Site { get; set; } = 0.0D;

        private double breakDownE_Field = 3100000D;

        [JsonProperty("breakDownEField")]
        public double BreakDownE_Field
        {
            get
            {
                //if (H_Site > 0.0)
                //{
                breakDownE_Field = 3100000D * (0.82 + 0.18 * (1 - 0.5 * (H_Site / 1000)));
                return breakDownE_Field;
                //}
                //else
                //{
                //    return breakDownE_Field;
                //}
            }
        }

        [JsonIgnore]
        public double CloudBase { get; set; } = 5000.00;

        [JsonIgnore]
        public double PeakCurrent { get; set; }

        [JsonIgnore]
        public double StrikingDistancePercentage { get; set; }

    }

    public class Top
    {
        [JsonProperty("x")]
        public double X { get; set; }

        [JsonProperty("y")]
        public double Y { get; set; }

        [JsonProperty("z")]
        public double Z { get; set; }

        public override bool Equals(object obj)
        {
            // Perform an equality check on two rectangles (Point object pairs).
            if (obj == null || GetType() != obj.GetType())
                return false;
            Top objectToCompare = (Top)obj;
            return X.Equals(objectToCompare.X) && Y.Equals(objectToCompare.Y) && Z.Equals(objectToCompare.Z);
        }

        public override int GetHashCode()
        {
            return Tuple.Create(X, Y, Z).GetHashCode();
        }
    }

    public class VelocityBoundaryPoint
    {
        [JsonProperty("x")]
        public double X { get; set; }

        [JsonProperty("y")]
        public double Y { get; set; }

        [JsonProperty("z")]
        public double Z { get; set; }

        public override bool Equals(object obj)
        {
            // Perform an equality check on two rectangles (Point object pairs).
            if (obj == null || GetType() != obj.GetType())
                return false;
            Top objectToCompare = (Top)obj;
            return X.Equals(objectToCompare.X) && Y.Equals(objectToCompare.Y) && Z.Equals(objectToCompare.Z);
        }

        public override int GetHashCode()
        {
            return Tuple.Create(X, Y, Z).GetHashCode();
        }
    }

    public class Position
    {
        [JsonProperty("x")]
        public double X { get; set; }

        [JsonProperty("y")]
        public double Y { get; set; }

        [JsonProperty("z")]
        public double Z { get; set; }


        public override bool Equals(object obj)
        {
            // Perform an equality check on two rectangles (Point object pairs).
            if (obj == null || GetType() != obj.GetType())
                return false;
            Position objectToCompare = (Position)obj;
            return X.Equals(objectToCompare.X) && Y.Equals(objectToCompare.Y) && Z.Equals(objectToCompare.Z);
        }
        public override int GetHashCode()
        {
            return Tuple.Create(X, Y, Z).GetHashCode();
        }
    }

    public class Position2
    {
        [JsonProperty("x")]
        public double X { get; set; }

        [JsonProperty("y")]
        public double Y { get; set; }

        [JsonProperty("z")]
        public double Z { get; set; }

        public override bool Equals(object obj)
        {
            // Perform an equality check on two rectangles (Point object pairs).
            if (obj == null || GetType() != obj.GetType())
                return false;
            Position2 objectToCompare = (Position2)obj;
            return X.Equals(objectToCompare.X) && Y.Equals(objectToCompare.Y) && Z.Equals(objectToCompare.Z);
        }
        public override int GetHashCode()
        {
            return Tuple.Create(X, Y, Z).GetHashCode();
        }

        public Position2(double x, double y, double z)
        {
            X = x; Y = y; Z = z;
        }
    }

    public class Point
    {
        [JsonProperty("attractiveRadius")]
        public double AttractiveRadius { get; set; }

        [JsonProperty("bottomPoint")]
        public BottomPoint BottomPoint { get; set; }

        [JsonProperty("companionCvmPointGuids")]
        public List<string> CompanionCvmPointGuids { get; set; } = new List<string>();

        [JsonProperty("dependentPointGuids")]
        public List<string> DependentPointGuids { get; set; } = new List<string>();

        [JsonProperty("extendedPoint")]
        public bool ExtendedPoint { get; set; }

        [JsonProperty("faceIndex")]
        public int FaceIndex { get; set; }

        [JsonProperty("faceNormal")]
        public FaceNormal FaceNormal { get; set; }

        [JsonProperty("heightOfAttractiveRadius")]
        public double HeightOfAttractiveRadius { get; set; }

        [JsonProperty("hostGuid")]
        public string HostGuid { get; set; }

        [JsonProperty("isCorner")]
        public bool IsCorner { get; set; }

        [JsonProperty("isEdgeRectangular")]
        public bool IsEdgeRectangular { get; set; }

        [JsonProperty("isEdgeOval")]
        public bool IsEdgeOval { get; set; }

        [JsonProperty("isCvmEdgePoint")]
        public bool IsCvmEdgePoint { get; set; }

        [JsonProperty("isFaceHorizontal")]
        public bool IsFaceHorizontal { get; set; }

        [JsonProperty("isFaceVertical")]
        public bool IsFaceVertical { get; set; }

        [JsonProperty("isGableEaveCorner")]
        public bool IsGableEaveCorner { get; set; }

        [JsonProperty("isGableEaveEdge")]
        public bool IsGableEaveEdge { get; set; }

        [JsonProperty("isGableRidgeCorner")]
        public bool IsGableRidgeCorner { get; set; }

        [JsonProperty("isGableRidgeEdge")]
        public bool IsGableRidgeEdge { get; set; }

        [JsonProperty("isGableRoof")]
        public bool IsGableRoof { get; set; }

        [JsonProperty("kiTotalContribution")]
        public double KiTotalContribution { get; set; }

        [JsonProperty("kiTotalMultiplicative")]
        public double TotalMultiplicative { get; set; }

        [JsonProperty("kiTotalReductive")]
        public double TotalReductive { get; set; }

        [JsonProperty("levelGuid")]
        public string LevelGuid { get; set; }

        [JsonProperty("parentPointGuid")]
        internal string ParentPointGuid;

        [JsonProperty("pointGuid")]
        public string PointGuid { get; set; }

        [JsonProperty("position")]
        public Position2 Position { get; set; }

        /** <summary>Describes who protected this object.</summary> */
        [JsonProperty("protecteBy")]
        internal string ProtectedBy;

        /** <summary>True to protected point.</summary> */
        [JsonProperty("protectedPoint")]
        internal bool ProtectedPoint;

        /** <summary>True if protection needed.</summary> */
        [JsonProperty("protectionNeeded")]
        internal bool ProtectionNeeded;

        [JsonProperty("protectionNote")]
        internal ResultsMessages ProtectionNote { get; set; }

        /** <summary>The rps.</summary> */
        [JsonProperty("rps")]
        internal double Rps;

        /** <summary>Unique identifier for the RS group.</summary> */
        [JsonProperty("rsGroupGuid")]
        internal string RsGroupGuid;

        [JsonProperty("magicPoint")]
        public Point MagicPoint { get; set; }

        [JsonProperty("magicNumber")]
        public double MagicNumber { get; set; }

        [JsonProperty("slope")]
        public double Slope { get; set; }

        [JsonIgnore]
        public KiDto KiData { get; set; }

        [JsonIgnore]
        public Level Level { get; set; }

        [JsonIgnore]
        public PoiLocation LocationOnStucture { get; set; }

        [JsonIgnore]
        public PoiLocation LocationOnLevelBelow { get; set; }

        [JsonIgnore]
        public int LevelOfProtection { get; set; }

        [JsonIgnore]
        public double Q_LeaderCharge { get; set; }

        [JsonIgnore]
        public bool IsExtendedCornerOrEdge { get; set; } = false;

        [JsonIgnore]
        public double H_Site { get; set; } = 0.0D;

        private double breakDownE_Field = 3100000D;
        [JsonIgnore]
        public double BreakDownE_Field
        {
            get
            {
                //if (H_Site > 0.0)
                //{
                breakDownE_Field = 3100000D * (0.82 + 0.18 * (1 - 0.5 * (H_Site / 1000)));
                return breakDownE_Field;
                //}
                //else
                //{
                //    return breakDownE_Field;
                //}
            }
        }

        [JsonIgnore]
        public double CloudBase { get; set; } = 5000.00;

        [JsonIgnore]
        public double PeakCurrent { get; set; }

        [JsonIgnore]
        public double StrikingDistancePercentage { get; set; }


        /**
        <summary>Attempts to identify edges by comparing slopes of points and grouping them AnalysisEdge
                 objects.</summary>
        <remarks>Carlo, 2/26/2021.</remarks>
        <param name="allPoints"> All of the analysis points.</param>
        <param name="userCookie">The user cookie.</param>
        <returns>Dictionary with level elevations as keys and lists of edges containing points that share
                 a similar slope in the xy-plane.</returns>
         */
        public static Dictionary<string, List<AnalysisEdge_CVM>> IdentifyEdges_CVM(List<Cvm.Level> levels, List<Cvm.Point> allPoints, UserCookie userCookie)
        {
            try
            {
                Dictionary<string, List<Cvm.Point>> groupedLevels = new Dictionary<string, List<Cvm.Point>>();

                foreach (Cvm.Level level in levels)
                {
                    //Join together the points to use for levels and group them by their rounded elevation into a dictionary.
                    List<Cvm.Point> pointsForLevels = allPoints.
                        Where(p => p.IsEdgeRectangular == true || p.IsEdgeOval == true || p.IsCorner == true).
                        Where(p => p.LevelGuid == level.LevelGuid).
                        ToList();
                    groupedLevels.Add(level.LevelGuid, pointsForLevels);
                }

                //Make a new dictionary to store edges by level, using the points from the level and points dictionary
                Dictionary<string, List<AnalysisEdge_CVM>> levelsAndEdges = new Dictionary<string, List<AnalysisEdge_CVM>>();

                //Cycle through each level by the key of the groupedLevels dictionary
                foreach (string levelGuid in groupedLevels.Keys)
                {
                    var level = levels.Where(l => l.LevelGuid == levelGuid).FirstOrDefault();
                    //Get all points for the level from the dictionary that could be corner or edge points
                    var edgePoints_Straight = groupedLevels[levelGuid].Where(p => p.IsEdgeRectangular || p.IsCorner).ToList();
                    var edgePoints_Curved = groupedLevels[levelGuid].Where(p => p.IsEdgeOval).ToList();

                    if (edgePoints_Straight.Count() > 0 || edgePoints_Curved.Count() > 0)
                    {
                        //List to store edges
                        List<AnalysisEdge_CVM> edges = new List<AnalysisEdge_CVM>();

                        if (edgePoints_Straight.Count > 0)
                        {
                            GetStraightEdges();

                            void GetStraightEdges()
                            {
                                //Add a new list of analysisEdge objects
                                levelsAndEdges[level.LevelGuid] = new List<AnalysisEdge_CVM>();

                                //The start of the edges loop could be a corner or edge. Start with the one that is most left on the x-axis
                                Cvm.Point minEdgePoint = edgePoints_Straight.OrderBy(p => p.Position.X).ThenBy(p => p.Position.Y).FirstOrDefault();
                                if (minEdgePoint == null) { return; }
                                Cvm.Point startPoint = minEdgePoint;

                                //List to store evaluated points
                                List<Cvm.Point> evaluatedPoints = new List<Cvm.Point>();
                                //List to remove points evaluated to prevent backtracking on closest points.
                                List<Cvm.Point> remainingPoints = edgePoints_Straight.ToList();

                                //Set the first point to act as the starting point.
                                Cvm.Point currentPoint = startPoint;
                                double maxDist = AnalysisEdge_CVM.controlDist;
                                AnalysisEdge_CVM previousEdge = null;
                                AnalysisEdge_CVM edge = null;

                                //Cycle through the points, starting in the direction based on the next closest point returned
                                for (int i = 0; i < edgePoints_Straight.Count(); i++)
                                {
                                    //The next point to use after the current point will be the one closest to the current point that has not been evaluated.
                                    dynamic next = GetClosestPoint_CVM(currentPoint, remainingPoints, userCookie);
                                    if (next == null)
                                    {
                                        break;
                                    }

                                    Cvm.Point nextPoint = GetClosestPoint_CVM(currentPoint, remainingPoints, userCookie);

                                    //Get the distance to see if the jump between points was greater than the maximum allowable spacing.
                                    dynamic dist = AnalysisPointData.GetHypotenuse2D(new threeVector3(currentPoint.Position.X, currentPoint.Position.Y, currentPoint.Position.Z), new threeVector3(nextPoint.Position.X, nextPoint.Position.Y, nextPoint.Position.Z));
                                    if (dist == null)
                                    {
                                        continue;
                                    }

                                    double distance = dist;

                                    //Get the vector angle in the xy-plane from the two points relative to the x-axis to track the direction
                                    double angle = Math.Round(threeVector3.GetAngleBetweenVectorsToXAxisInXYPlane(new threeVector3(currentPoint.Position.X, currentPoint.Position.Y, currentPoint.Position.Z), new threeVector3(nextPoint.Position.X, nextPoint.Position.Y, nextPoint.Position.Z)) * 180 / Math.PI);
                                    if (nextPoint.Position.Y - currentPoint.Position.Y < 0)
                                    {
                                        angle = -angle;
                                    }

                                    double deviation = previousEdge != null ? Math.Round(Math.Floor(currentPoint.Position.Z) - (previousEdge.elevation)) : 0;
                                    if (angle == previousEdge?.angle && deviation <= 1d && distance < maxDist)
                                    {
                                        //If the angle is equal to the previous edge, use the previous edge
                                        edge = previousEdge;
                                    }
                                    else if (distance > maxDist || deviation >= 1d)
                                    {
                                        //Else create a new one
                                        edge = new AnalysisEdge_CVM
                                        {
                                            elevation = Math.Floor(currentPoint.Position.Z),
                                            curvedEdge = false,
                                        };
                                        edges.Add(edge);
                                    }
                                    else
                                    {
                                        //Else create a new one
                                        edge = new AnalysisEdge_CVM
                                        {
                                            elevation = Math.Floor(currentPoint.Position.Z),
                                            curvedEdge = false,
                                        };
                                        edges.Add(edge);
                                    }

                                    //Set the angle
                                    edge.angle = edge.angle == AnalysisEdge_CVM.controlAngle ? angle : edge.angle;


                                    //If the edge does not contain the current point, add it to the edge, and remove it from the remaining points.
                                    if (edge.points.Find(p => p.PointGuid == currentPoint.PointGuid) == null)
                                    {
                                        edge.points.Add(currentPoint);
                                        evaluatedPoints.Add(currentPoint);
                                        remainingPoints.Remove(currentPoint);
                                    }
                                    //If the edge does not contain the next point, add it to the edge, and remove it from the remaining points.
                                    if (edge.points.Find(p => p.PointGuid == nextPoint.PointGuid) == null)
                                    {
                                        edge.points.Add(nextPoint);
                                        evaluatedPoints.Add(nextPoint);
                                        remainingPoints.Remove(currentPoint);
                                    }

                                    //The start point of the edge should be the 
                                    edge.startPoint = edge.points.OrderBy(p => p.Position.X).First();
                                    edge.endPoint = edge.points.OrderByDescending(p => p.Position.X).First();

                                    previousEdge = edge;

                                    //Set the current point to the next point and move on to the next closest point
                                    currentPoint = nextPoint;
                                }
                            }
                        }

                        if (edgePoints_Curved.Count > 0)
                        {
                            GetCurvedEdges();

                            void GetCurvedEdges()
                            {
                                //Add a new list of analysisEdge objects
                                levelsAndEdges[level.LevelGuid] = new List<AnalysisEdge_CVM>();

                                //The start of the edges loop could be a corner or edge. Start with the one that is most left on the x-axis
                                Cvm.Point minEdgePoint = edgePoints_Curved.OrderBy(p => p.Position.X).ThenBy(p => p.Position.Y).FirstOrDefault();
                                if (minEdgePoint == null) { return; }
                                Cvm.Point startPoint = minEdgePoint;

                                //List to store evaluated points
                                List<Cvm.Point> evaluatedPoints = new List<Cvm.Point>();
                                //List to remove points evaluated to prevent backtracking on closest points.
                                List<Cvm.Point> remainingPoints = edgePoints_Curved.ToList();

                                //Set the first point to act as the starting point.
                                Cvm.Point currentPoint = startPoint;
                                double maxDist = AnalysisEdge_CVM.controlDist;
                                AnalysisEdge_CVM previousEdge = null;
                                AnalysisEdge_CVM edge = null;

                                //Cycle through the points, starting in the direction based on the next closest point returned
                                for (int i = 0; i < edgePoints_Curved.Count(); i++)
                                {
                                    //The next point to use after the current point will be the one closest to the current point that has not been evaluated.
                                    dynamic next = GetClosestPoint_CVM(currentPoint, remainingPoints, userCookie);
                                    if (next == null)
                                    {
                                        break;
                                    }

                                    Cvm.Point nextPoint = GetClosestPoint_CVM(currentPoint, remainingPoints, userCookie);

                                    //Get the distance to see if the jump between points was greater than the maximum allowable spacing.
                                    dynamic dist = AnalysisPointData.GetHypotenuse2D(new threeVector3(currentPoint.Position.X, currentPoint.Position.Y, currentPoint.Position.Z), new threeVector3(nextPoint.Position.X, nextPoint.Position.Y, nextPoint.Position.Z));
                                    if (dist == null)
                                    {
                                        continue;
                                    }

                                    double distance = dist;

                                    //Get the vector angle in the xy-plane from the two points relative to the x-axis to track the direction
                                    double angle = Math.Round(threeVector3.GetAngleBetweenVectorsToXAxisInXYPlane(new threeVector3(currentPoint.Position.X, currentPoint.Position.Y, currentPoint.Position.Z), new threeVector3(nextPoint.Position.X, nextPoint.Position.Y, nextPoint.Position.Z)) * 180 / Math.PI);
                                    if (nextPoint.Position.Y - currentPoint.Position.Y < 0)
                                    {
                                        angle = -angle;
                                    }

                                    double deviation = previousEdge != null ? Math.Round(Math.Floor(currentPoint.Position.Z) - (previousEdge.elevation)) : 0;
                                    if (distance > maxDist || deviation >= 1d)
                                    {
                                        //Else create a new one
                                        edge = new AnalysisEdge_CVM
                                        {
                                            elevation = Math.Floor(currentPoint.Position.Z),
                                            curvedEdge = true,
                                        };
                                        edges.Add(edge);
                                    }
                                    else
                                    {
                                        //Else create a new one
                                        edge = new AnalysisEdge_CVM
                                        {
                                            elevation = Math.Floor(currentPoint.Position.Z),
                                            curvedEdge = true,
                                        };
                                        edges.Add(edge);
                                    }

                                    //Set the angle
                                    edge.angle = edge.angle == AnalysisEdge_CVM.controlAngle ? angle : edge.angle;

                                    //If the edge does not contain the current point, add it to the edge, and remove it from the remaining points.
                                    if (edge.points.Find(p => p.PointGuid == currentPoint.PointGuid) == null)
                                    {
                                        edge.points.Add(currentPoint);
                                        evaluatedPoints.Add(currentPoint);
                                        remainingPoints.Remove(currentPoint);
                                    }
                                    //If the edge does not contain the next point, add it to the edge, and remove it from the remaining points.
                                    if (edge.points.Find(p => p.PointGuid == nextPoint.PointGuid) == null)
                                    {
                                        edge.points.Add(nextPoint);
                                        evaluatedPoints.Add(nextPoint);
                                        remainingPoints.Remove(currentPoint);
                                    }

                                    //The start point of the edge should be the 
                                    edge.startPoint = edge.points.OrderBy(p => p.Position.X).First();
                                    edge.endPoint = edge.points.OrderByDescending(p => p.Position.X).First();

                                    previousEdge = edge;

                                    //Set the current point to the next point and move on to the next closest point
                                    currentPoint = nextPoint;
                                }
                            }
                        }

                        List<AnalysisEdge_CVM> actualEdges = CleanupEdges(edges);


                        //All points by level, separated into multi-point edges or single point edges.
                        levelsAndEdges[level.LevelGuid] = actualEdges.ToList();
                    }
                }

                //Add all the companion point GUIDs within the same edge
                foreach (var analysisEdges in levelsAndEdges.Values.ToList())
                {
                    foreach (var analysisEdge in analysisEdges.ToList())
                    {
                        var edgePoints = analysisEdge.points.Where(p => !p.IsCorner).Select(p => p).ToList();

                        foreach (var edgePoint in edgePoints)
                        {
                            edgePoint.CompanionCvmPointGuids = edgePoints.Where(p => p.PointGuid != edgePoint.PointGuid).Select(p => p.PointGuid).ToList();
                        }
                    }
                }

                //Return the levels and edges dictionary
                return levelsAndEdges;
            }
            catch (Exception ex)
            {
                string className = "AnalysisPointData";
                string methodName = "IdentifyEdges";
                LogReport report = new LogReport(className, methodName, LogLevel.High, ex.Message, ex.StackTrace, userCookie, new { });
                report.WriteReport();
                return null;
            }

            static List<AnalysisEdge_CVM> CleanupEdges(List<AnalysisEdge_CVM> edges)
            {
                var singleEdges = edges.Where(e => e.points.Count == 1).ToList();
                var cornerEdges = edges.Where(e => e.points.Count == 2).ToList();
                var actualEdges = edges.Where(e => e.points.Count > 2).ToList();
                foreach (var cornerEdge in cornerEdges)
                {
                    var point0 = cornerEdge.points[0];
                    var point1 = cornerEdge.points[1];
                    var commonedge = actualEdges?.Where(e => e.points.Contains(point0) || e.points.Contains(point1));
                    if (commonedge.ToList().Count != 0)
                    {
                        var ce = commonedge.First();
                        if (!ce.points.Contains(point0))
                        {
                            ce.points.Add(point0);
                        }
                        if (!ce.points.Contains(point1))
                        {
                            ce.points.Add(point1);
                        }
                    }
                }
                // get the midpoints of the edges for CVM analysis
                foreach (var edgeObj in actualEdges.ToList())
                {
                    var edgeCount = edgeObj.points.Count;

                    var edgeCountIsEven = edgeCount % 2 == 0;

                    if (edgeCountIsEven) // If number of edge points is even
                    {
                        var index = (edgeCount - 1) / 2;
                        edgeObj.cvmEdgePoint = edgeObj.points[index];
                    }
                    else // If number of edge points is odd
                    {
                        var index = ((edgeCount - 1) / 2) + 1;
                        edgeObj.cvmEdgePoint = edgeObj.points[index];
                    }
                }

                //Might occur if the spacing between edge points is greater than 5 m. If so, treat each one as its own edge.
                foreach (var pointEdge in singleEdges)
                {
                    if (pointEdge.points[0].IsEdgeOval || pointEdge.points[0].IsEdgeRectangular)
                    {
                        actualEdges.Add(pointEdge);
                    }
                }

                return actualEdges;
            }
        }

        /**
        <summary>Gets closest point cvm.</summary>
        <remarks>Carlo, 4/6/2021.</remarks>
        <param name="currentPoint">The currently being evaluated point.</param>
        <param name="points">      The points to compare to the current point.</param>
        <param name="userCookie">  The user cookie.</param>
        <returns type="dynamic">The closest point cvm.</returns>
         */
        private static dynamic GetClosestPoint_CVM(Cvm.Point currentPoint, List<Cvm.Point> points, UserCookie userCookie)
        {
            Cvm.Point closestPoint = null;
            double dist = 5000;

            try
            {
                //Only evaluate a list with points
                if (points.Count > 0)
                {
                    //If the number of points is 1 and the only point is the current point, return null
                    if (points.Count == 1 && points[0].PointGuid == currentPoint.PointGuid)
                    {
                        return null;
                    }

                    //Otherwise cycle through the points
                    foreach (Cvm.Point point in points)
                    {
                        //Don't evaluate the current point against itself
                        if (point.PointGuid != currentPoint.PointGuid)
                        {
                            //If a point has not been evaluated the closest point is the point being compared
                            if (closestPoint == null)
                            {
                                closestPoint = point;
                            }
                            else
                            {
                                //Compare the distance between the comparison point and the current point.
                                var dist1 = GetHypotenuse2D_CVM(currentPoint.Position, point.Position);
                                if (dist1 < dist)
                                {
                                    //If the distance is less than the current shortest distance, it is the new shortest distance;
                                    dist = dist1;
                                    //The point being evaluated is now the closest point.
                                    closestPoint = point;
                                }
                                //Comparison if there are two points equidistant from the current point. if so take the point wit 
                                if (dist1 == dist)
                                {
                                    if (closestPoint.Position.X < point.Position.X)
                                    {
                                        threeVector3 vector0 = new threeVector3(1, 0, 0);
                                        //Switch to Vector3 for ease of normalization
                                        Vector3 vector1 = new Vector3(Convert.ToSingle(point.Position.X), Convert.ToSingle(point.Position.Y), Convert.ToSingle(point.Position.Z));
                                        Vector3 unitVector1 = Vector3.Normalize(vector1);
                                        Vector3 vector2 = new Vector3(Convert.ToSingle(closestPoint.Position.X), Convert.ToSingle(closestPoint.Position.Y), Convert.ToSingle(closestPoint.Position.Z));
                                        Vector3 unitVector2 = Vector3.Normalize(vector2);

                                        //Convert back to threeVector3
                                        threeVector3 v1 = new threeVector3(unitVector1.X, unitVector1.Y, unitVector1.Z);
                                        threeVector3 v2 = new threeVector3(unitVector2.X, unitVector2.Y, unitVector2.Z);

                                        var angle1rads = threeVector3.GetAngleBetweenVectorsToXAxisInXYPlane(vector0, v1);
                                        var angle2rads = threeVector3.GetAngleBetweenVectorsToXAxisInXYPlane(vector0, v2);

                                        var angle1 = angle1rads * 180 / Math.PI;
                                        var angle2 = angle1rads * 180 / Math.PI;

                                        //Closest point should be the one that has a smaller angle to the x axis such that to evaluate points clockwise.
                                        if (angle1 < angle2)
                                        {
                                            closestPoint = point;
                                        }
                                    }
                                }
                            }
                        }
                    }

                    //Return the closest point
                    return closestPoint;
                }
                else
                {
                    //Return null if the list is empty
                    return null;
                }
            }
            catch (Exception ex)
            {
                string className = "AnalysisPointData";
                string methodName = "GetClosestEdge";
                LogReport report = new LogReport(className, methodName, LogLevel.High, ex.Message, ex.StackTrace, userCookie, new { });
                report.WriteReport();
                return null;
            }
        }

        /**
        <summary>Gets the hypotenuse of two 3D points.</summary>
        <remarks>Carlo, 2/26/2021.</remarks>
        <param name="point0">The point 0.</param>
        <param name="point1">The first point.</param>
        <returns>Length.</returns>
         */
        internal static dynamic GetHypotenuse2D_CVM(Cvm.Position2 point0, Cvm.Position2 point1)
        {
            double x1 = point0.X;
            double y1 = point0.Y;
            double x2 = point1.X;
            double y2 = point1.Y;

            double lengthxyz = Math.Sqrt(Math.Pow(x2 - x1, 2) + Math.Pow(y2 - y1, 2));

            return lengthxyz;
        }

    }

    public class CVMData
    {
        [JsonProperty("site")]
        public Site Site { get; set; }

        [JsonProperty("terminals")]
        public IList<Terminal> Terminals { get; set; }

        [JsonProperty("points")]
        public IList<Point> Points { get; set; }

        [JsonProperty("levels")]
        public IList<Level> Levels { get; set; }

        [JsonProperty("buildings")]
        public IList<Building> Buildings { get; set; }

        [JsonProperty("standard")]
        internal string standard { get; set; }

        [JsonProperty("hazardous")]
        internal bool hazardous { get; set; }

        [JsonProperty("reduce")]
        internal bool reduce { get; set; }

        public CVMData()
        {
            Site = new Site();
            Terminals = new List<Terminal>();
            Points = new List<Point>();
            Levels = new List<Level>();
            Buildings = new List<Building>();
            standard = "";
            hazardous = false;
            reduce = false;
        }
    }

    #endregion CVM JSON Data

    #region Level Class

    public class Level
    {
        /**
         * <summary>Gets or sets the bounding box of the level based on the level's points and level above points, oriented aligned to the XY axis</summary>
         * <value>The bounding box.</value>
         */
        [JsonProperty("boundingBox")]
        public BoundingBox BoundingBox { get; set; }

        /**
         * <summary>Gets or sets the convex hull points that define the footprint of the level</summary>
         * <value>The convex hull points.</value>
         */
        [JsonProperty("convexHullPoints")]
        public List<threeVector3> ConvexHullPoints { get; set; }

        /**
         * <summary>Gets or sets the level's elevation</summary>
         * <value>The level elevation.</value>
         */
        [JsonProperty("elevation")]
        public double ForgeLevelElevation { get; set; }

        /**
         * <summary>Gets or sets a unique identifier for the host model of the level</summary>
         * <value>Unique identifier for the host.</value>
         */
        [JsonIgnore]
        public double MinimumReductiveDistance
        {
            get
            {
                double d_min;
                double H = ForgeLevelElevation;
                double W;

                if (BoundingBox != null)
                {
                    W = BoundingBox.MinimumWidth;
                    // 𝑑_𝑚𝑖𝑛=(3.8𝐻_2^0.78 𝑊_2^0.28)/2
                    d_min = 3.8 * Math.Pow(H, 0.78) * Math.Pow(W, 0.28) / 2;
                    return d_min;
                }
                else
                {
                    return 1.0D;
                }
            }
        }

        [JsonIgnore]
        public bool IsSlender
        {
            get
            {
                // Determine if there are structures above -- Determining this could be problematic
                if (BoundingBox != null && HeightJustThisLevel > 0)
                {
                    double H = HeightJustThisLevel;
                    double W = BoundingBox.MinimumWidth;

                    double sRatio = H / W;

                    if (BoundingBox.MinimumWidth < 2.0 || sRatio > 50.0D)
                    {
                        return true;
                    }
                    else
                    {
                        return false;
                    }

                }
                else
                {
                    return false;
                }
            }
        }

        [JsonProperty("hostGuid")]
        public string HostGuid { get; set; }

        /**
         * <summary>Gets or sets a value indicating whether this level is a sub level</summary>
         * <value>True if this level is a sub level, false if not.</value>
         */
        [JsonProperty("isSubLevel")]
        public bool IsSubLevel { get; set; }

        /**
         * <summary>Gets or sets the levels above as a dictionary with the elevation as the key and the level as the value.</summary>
         * <value>The levels above.</value>
         */
        [JsonProperty("levelsAbove")]
        public List<string> LevelsAbove { get; set; } = new List<string>();

        /**
         * <summary>Gets or sets a unique identifier for the level</summary>
         * <value>Unique identifier for the level.</value>
         */
        [JsonProperty("levelGuid")]
        public string LevelGuid { get; set; }

        /**
         * <summary>Gets or sets the name of the level</summary>
         * <value>The name of the level.</value>
         */
        [JsonProperty("levelName")]
        public string LevelName { get; set; }

        /**
         * <summary>Gets or sets the level number</summary>
         * <value>The level number.</value>
         */
        [JsonProperty("levelNumber")]
        public double LevelNumber { get; set; }

        /**
         * <summary>Gets or sets a unique identifier for the parent level of this level</summary>
         * <value>Unique identifier for the parent level.</value>
         * <remarks>This will be an empty string if the level has no parent (IsSubLevel is false).</remarks>
         */
        [JsonProperty("parentLevelGuid")]
        public string ParentLevelGuid { get; set; }

        [JsonIgnore]
        public double ElevationForKi { get; set; }

        [JsonIgnore]
        public bool TopMost { get; set; } = false;

        [JsonIgnore]
        public PoiLocation PointOfInterestLocation { get; set; }

        [JsonIgnore]
        public LevelShape LevelShape { get; set; }

        [JsonIgnore]
        public Level NextLevelBelow { get; set; }

        /**
         * <summary>Gets or sets a value indicating whether this object is a sub level parent</summary>
         * <value>True if this object is sub level parent, false if not.</value>
         */
        [JsonIgnore]
        public bool IsSubLevelParent { get; set; }

        [JsonIgnore]
        public List<string> LevelsBelow { get; set; } = new List<string>();

        [JsonIgnore]
        public List<Level> LevelsAboveInOtherBuildings { get; set; } = new List<Level>();

        [JsonIgnore]
        public double MinimumDistanceToOtherBuildings
        {
            get
            {
                //𝑑_𝑚𝑖𝑛=(3.8𝐻_2^0.78 𝑊_2^0.28)/2
                double minDistance = (Math.Pow(3.8 * ForgeLevelElevation, 0.78) * Math.Pow(3.8 * MinimumWidth, 0.28)) / 2;
                return minDistance;
            }
        }

        [JsonIgnore]
        public double NearestPointRangeDistance { get; set; } = 2.0D;

        [JsonIgnore]
        public bool IsGabel { get; set; } = false;

        [JsonIgnore]
        public double GabelHeight { get; set; } = 1.0D;

        [JsonIgnore]
        public bool IsRectangular { get; set; } = false;

        [JsonIgnore]
        public bool IsOval { get; set; } = false;

        [JsonIgnore]
        public bool IsHybrid { get; set; } = false;

        [JsonIgnore]
        public bool IsExtendedFeature { get; set; } = false;

        [JsonIgnore]
        public bool HasLevelAbove { get; set; } = false;

        [JsonIgnore]
        public bool HasLevelBelow { get; set; } = false;

        [JsonProperty("minWidth")]
        public double MinimumWidth
        {
            get
            {
                return BoundingBox.MinimumWidth;
            }
        }

        [JsonIgnore]
        public double GableWidth { get; set; }

        [JsonIgnore]
        public GableShape GableShape { get; set; }

        [JsonIgnore]
        public double HeightJustThisLevel { get; set; }

        [JsonIgnore]
        public List<threeBox3> BoundingBoxCentroid { get; set; }

        [JsonIgnore]
        public List<Point> PointsByLevelGuid { get; set; } = new List<Point>();

        [JsonIgnore]
        public List<Point> PointsBySubLevelGuid { get; set; } = new List<Point>();

        [JsonIgnore]
        public List<Point> EdgePointsOval { get; set; } = new List<Point>();

        [JsonIgnore]
        public List<Point> GableEaveEdges { get; set; } = new List<Point>();

        [JsonIgnore]
        public List<Point> GableSlopedEdges { get; set; } = new List<Point>();

        [JsonIgnore]
        public List<Point> GableRidgeEdges { get; set; } = new List<Point>();

        [JsonIgnore]
        public List<Point> GableEaveCorners { get; set; } = new List<Point>();

        [JsonIgnore]
        public List<Point> GableRidgeCorners { get; set; } = new List<Point>();

        [JsonIgnore]
        public List<Point> EdgePointsRectangular { get; set; } = new List<Point>();

        [JsonIgnore]
        public List<Point> Corners { get; set; } = new List<Point>();

        [JsonIgnore]
        public List<Point> CvmEdgePoints { get; set; } = new List<Point>();

        [JsonIgnore]
        public List<Point> HorizontalPoints { get; set; } = new List<Point>();

        [JsonIgnore]
        public List<Terminal> DynosphereAirTerminals { get; set; } = new List<Terminal>();

        [JsonIgnore]
        public List<Terminal> PassiveAirTerminals { get; set; } = new List<Terminal>();

        [JsonIgnore]
        public List<Point> PointsAboveLevel { get; set; } = new List<Point>();

        public Level()
        {

        }

        public Level(int levelNumber,
                            double levelHeight,
                            string buildingGuid,
                            List<Point> cornerPoints,
                            List<Point> edgePointsRectangular,
                            List<Point> edgePointsOval,
                            List<Point> horizontalPoints)
        {
            HostGuid = buildingGuid;
            LevelNumber = levelNumber;
            ForgeLevelElevation = levelHeight;
            Corners = cornerPoints;
            EdgePointsRectangular = edgePointsRectangular;
            EdgePointsOval = edgePointsOval;
            HorizontalPoints = horizontalPoints;
            initValues();
        }

        public void initValues()
        {

            //IsGabel = EdgePointsGable.Any();
            //IsRectangular = EdgePointsRectangular.Any();
            //IsOval = EdgePointsOval.Any();

            //if (EdgePointsRectangular.Count > 0)
            //{
            //    IsGabel = EdgePointsGable.Any();

            //    IsRectangular = true;
            //}

            //if (EdgePointsOval.Count > 0)
            //{
            //    IsOval = true;
            //}

            //CalculateWidthOfThisLevel();
        }

        //public void AssembleEdgesForLevel()
        //{
        //    var isGabel = false;
        //    try
        //    {
        //        var levelEdge = new LevelEdge();

        //        LevelShape edgeType = LevelShape.NotSet;

        //        if (EdgePointsRectangular.Count > 0)
        //        {
        //            edgeType = LevelShape.Rectangle;
        //            levelEdge.EdgePoints = EdgePointsRectangular;
        //        }
        //        if (EdgePointsOval.Count > 0)
        //        {
        //            edgeType = LevelShape.Oval;
        //            levelEdge.EdgePoints = EdgePointsOval;
        //        }

        //        // Level contains an even number of corners greater than 1
        //        //if (cornerPointsThisLevel.Count > 1 && cornerPointsThisLevel.Count % 2 == 0)
        //        if (Corners.Count > 1)
        //        {
        //            for (int i = 0; i < Corners.Count; i++)
        //            {
        //                levelEdge.FirstCourner = Corners[i];

        //                for (int u = 1; u < Corners.Count; u++)
        //                {
        //                    levelEdge.SecondCorner = Corners[u];

        //                    foreach (var point in levelEdge.EdgePoints.ToList())
        //                    {
        //                        if (levelEdge.FirstCourner.IsGableRoof || levelEdge.SecondCorner.IsGableRoof) { isGabel = true; }

        //                        BottomPoint[] pointsToCompare = { levelEdge.FirstCourner.BottomPoint, point.BottomPoint, levelEdge.SecondCorner.BottomPoint };

        //                        var areCollinear = PointsAreCollinear(pointsToCompare, isGabel);

        //                        if (areCollinear)
        //                        {
        //                            levelEdge.EdgePoints.Add(point);
        //                        }
        //                    }
        //                }
        //            }

        //            //if (levelEdge.EdgePoints.Count > 0)
        //            //{
        //            //    if (edgeType == StructureShape.Rectangle)
        //            //    {
        //            //        EdgesRectagular.Add(levelEdge);
        //            //    }
        //            //    if (edgeType == StructureShape.Oval)
        //            //    {
        //            //        EdgesOval.Add(levelEdge);
        //            //    }
        //            //}
        //        }

        //        // Level contains an odd number of corners greater than 1
        //        //if (cornerPointsThisLevel.Count > 1 && cornerPointsThisLevel.Count % 2 != 0)
        //        //{

        //        //}

        //    }
        //    catch (Exception ex)
        //    {
        //        throw ex;
        //    }
        //}

        /// <summary> Calculates the width of this level. 
        ///           if the level is rectangular or is a gable roof
        ///           Note: the level must contain at least 3 corners</summary>
        ///
        /// <exception cref="Exception"> Thrown when an exception error condition occurs. </exception>
        //public void CalculateWidthOfThisLevel()
        //{
        //    try
        //    {

        //       // var results = new List<double>();

        //        //// if (this.IsRectangular && !this.IsGabel)
        //        // {
        //        //     var cornerArray = Corners.ToArray();

        //        //     var vectorPoints = new List<threeVector3>();

        //        //     if (Corners.Count > 2)
        //        //     {
        //        //         foreach (var corner in Corners)
        //        //         {
        //        //             var newVector = new threeVector3(corner.BottomPoint.X, corner.BottomPoint.Y, corner.BottomPoint.Z);
        //        //             vectorPoints.Add(newVector);
        //        //         }

        //        //         Tuple<threeVector3, threeVector3, double, threeVector3> bb = AnalysisPointData.GetOrientedBoundingBox(vectorPoints);

        //        //         if (Corners.Count >= 2)
        //        //         {
        //        //             for (int i = 0; i < cornerArray.Length - 1; i++)
        //        //             {
        //        //                 var thisCorner = Corners[i];
        //        //                 var nextCorner = Corners[i + 1];
        //        //                 results.Add(Math.Round(Math.Sqrt(Math.Pow((thisCorner.Position.X - nextCorner.Position.X), 2) + Math.Pow((thisCorner.Position.Y - nextCorner.Position.Y), 2)), 1));
        //        //             }

        //        //             var widths = results.OrderByDescending(l => l).ToList();

        //        //             MinimumWidth = widths.Min();
        //        //         }
        //        //     }
        //        // }
        //    }
        //    catch (Exception ex)
        //    {
        //        throw ex;
        //    }
        //}



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
                }
                if (ApproximatelyEqualDoubles(result, 0)) { return true; }
                else { return false; }
            }
            catch (Exception)
            {
                return false;
            }
        }

        /// <summary>
        /// Method determines if two doubles are roughly equivalent
        /// </summary>
        /// <param name="d1">first double value</param>
        /// <param name="d2">second double value</param>
        /// <param name="epsilon">the tolerance factor</param>
        /// <returns>Returns true if equivalent, otherwise false</returns>
        protected bool ApproximatelyEqualDoubles(double d1, double d2, double epsilon = 0.1255D)
        {
            return Math.Abs(d1 - d2) < epsilon;
        }
    }

    public class BoundingBox
    {
        [JsonProperty("min")]
        public threeVector3 MinPoint { get; set; }

        [JsonProperty("max")]
        public threeVector3 MaxPoint { get; set; }

        [JsonProperty("minWidth")]
        public double MinimumWidth { get; set; }

        [JsonIgnore]
        public threeVector3 BoundingBoxCentroid { get; set; }

        [JsonIgnore]
        public threeVector3 MinLeft { get; set; }

        [JsonIgnore]
        public threeVector3 MaxLeft { get; set; }

        [JsonIgnore]
        public threeVector3 MinRight { get; set; }

        [JsonIgnore]
        public threeVector3 MaxRight { get; set; }

        [JsonIgnore]
        public List<threeVector3> BoundingBoxPoints { get; set; } = new List<threeVector3>();

        [JsonIgnore]
        public List<threeVector3> OrientedBoundingBoxPoints { get; set; } = new List<threeVector3>();

        [JsonIgnore]
        public double OrientationAngle { get; set; }

        public BoundingBox()
        {
        }

        /// <summary>
        /// Returns a tuple of the bounding box points and its centroid based on the min and max points passed in.
        /// </summary>
        ///
        /// <param name="minPoint"> threeVector3 bounding box min point. </param>
        /// <param name="maxPoint"> threeVector3 bounding box max point. </param>
        ///
        /// <returns> a tuple. </returns>
        public void SetCentroidAndPoints(threeVector3 minPoint, threeVector3 maxPoint, List<threeVector3> convexHullPoints)
        {

            List<threeVector3> boundingBoxPoints = new List<threeVector3>();

            // Bounding Box points ordered clockwise, starting at the (x max, y max) point
            // Note: the IsPointInPolygon method ignores all Z values;
            // (max, max)
            threeVector3 maxRight = new threeVector3(maxPoint.x, maxPoint.y, minPoint.z);
            MaxRight = maxRight;
            boundingBoxPoints.Add(maxRight);

            // (max, min)
            threeVector3 minRight = new threeVector3(maxPoint.x, minPoint.y, minPoint.z);
            MinRight = minRight;
            boundingBoxPoints.Add(minRight);

            // (min, min)
            threeVector3 minLeft = new threeVector3(minPoint.x, minPoint.y, maxPoint.z);
            MinLeft = minLeft;
            boundingBoxPoints.Add(minLeft);

            // (min, max)
            threeVector3 maxLeft = new threeVector3(minPoint.x, maxPoint.y, maxPoint.z);
            MaxLeft = maxLeft;
            boundingBoxPoints.Add(maxLeft);

            BoundingBoxPoints = boundingBoxPoints;

            BoundingBoxCentroid = AnalysisPointData.GetCentroid3D(boundingBoxPoints);

            //var tuple = new Tuple<List<threeVector3>, threeVector3>(boundingBoxPoints, BoundingBoxCentroid);

            //return tuple;
        }

        /// <summary> Calculates the minimum width of the level's bounding box. </summary>
        public double CalculateMinimumWidth(List<threeVector3> convexHullPoints)
        {
            if (convexHullPoints.Count > 0)
            {
                //Returns the minimum and maximum point along with the angle of the box
                //Tuple<threeVector3, threeVector3, double, threeVector3> results = AnalysisPointData.GetOrientedBoundingBox(BoundingBoxPoints);
                Tuple<threeVector3, threeVector3, double, threeVector3> results = AnalysisPointData.GetOrientedBoundingBox(convexHullPoints);

                List<threeVector3> orientedBoundingBoxPoints = new List<threeVector3>();

                threeVector3 minPoint = results.Item1;
                threeVector3 maxPoint = results.Item2;
                OrientationAngle = results.Item3;

                // Bounding Box points ordered clockwise, starting at the (x max, y max) point
                // Note: the IsPointInPolygon method ignores all Z values;
                // (max, max)
                threeVector3 maxRight = new threeVector3(maxPoint.x, maxPoint.y, minPoint.z);
                orientedBoundingBoxPoints.Add(maxRight);

                // (max, min)
                threeVector3 minRight = new threeVector3(maxPoint.x, minPoint.y, minPoint.z);
                orientedBoundingBoxPoints.Add(minRight);

                // (min, min)
                threeVector3 minLeft = new threeVector3(minPoint.x, minPoint.y, maxPoint.z);
                orientedBoundingBoxPoints.Add(minLeft);

                // (min, max)
                threeVector3 maxLeft = new threeVector3(minPoint.x, maxPoint.y, maxPoint.z);
                orientedBoundingBoxPoints.Add(maxLeft);

                List<double> lengths = new List<double>();

                // Working Clockwise:
                var length1 = GetHypotenuse2D(maxRight, minRight);
                lengths.Add(length1);

                var length2 = GetHypotenuse2D(minRight, minLeft);
                lengths.Add(length2);

                var length3 = GetHypotenuse2D(maxLeft, minLeft);
                lengths.Add(length3);

                var length4 = GetHypotenuse2D(maxRight, maxLeft);
                lengths.Add(length4);

                return lengths.Min();
            }
            return 0;
        }

        /// <summary> Gets hypotenuse 2D. </summary>
        ///
        /// <param name="point0"> The point 0. </param>
        /// <param name="point1"> The first point. </param>
        internal double GetHypotenuse2D(threeVector3 point0, threeVector3 point1)
        {
            double x1 = point0.x;
            double y1 = point0.y;
            double x2 = point1.x;
            double y2 = point1.y;

            double lengthxyz = Math.Sqrt(Math.Pow(x2 - x1, 2) + Math.Pow(y2 - y1, 2));

            return lengthxyz;
        }
    }

    public class Rectangle
    {

    }

    #endregion Level Class

    #region Ki Data Transfer Object

    /// <summary> An in memory data transfer object to
    ///           accumulate Ki values and calculate the total KI contribution results. </summary>
    public class KiDto
    {
        [JsonProperty("kiForPoi")]
        /// <summary> Gets or sets the ki for dynasphere air terminal. </summary>
        public double KiForPoi { get; set; } = 1.00;

		[JsonProperty("firAtPoi")]
		/// <summary> Gets or sets the FIR (field intensification ratio) at the point of interest. </summary>
		public double FirAtPoi { get; set; } = 1.00;

		[JsonProperty("kiForStructureAtPoi")]
		/// <summary> Gets or sets the ki for structure at the point of interest. </summary>
		public double KiForStructureAtPoi { get; set; }

		[JsonProperty("totalMultiplicativeKiOnStructure")]
		public double TotalMultiplicativeKiOnStructure { get; set; } = 1.00;

		[JsonProperty("totalReductiveFactorOnStructure")]
		public double TotalReductiveFactorOnStructure { get; set; } = 1.00;

		[JsonIgnore]
		public double TotalReductiveFactorOnDynasphere { get; set; } = 1.00;

		[JsonProperty("totalKiContribution")]
		/// <summary> Gets or sets the total number of ki contribution. </summary>
		public double TotalKiContribution { get; set; }

        /// <summary> Gets or sets the total number of ki contribution. </summary>
        public bool DynasphereIsOnMast { get; set; } = false;

        /// <summary> Gets or sets a dictionary of multiplicative results. </summary>
        public Dictionary<string, double> MultiplicativeResultDictionary { get; set; } = new Dictionary<string, double>();

        /// <summary> Gets or sets poi positions and their elevations for complex ki calculations. </summary>

        /// <summary> Default constructor. </summary>
        public KiDto()
        {

        }

        /// <summary> Constructor. </summary>
        /// <param name="kiForTerminal"> The ki for dynasphere air terminal. </param>
        /// <param name="firAtPoi"> The FIR at this POI. </param>
        /// <param name="kiForStructure"> The ki for the structure at this POI. </param>
        public KiDto(double kiForTerminal, double firAtPoi, double kiForStructure)
        {
            KiForPoi = kiForTerminal;
            FirAtPoi = firAtPoi;
            KiForStructureAtPoi = kiForStructure;
        }

        /// <summary> Calculates the ki multiplicative effects. </summary>
        public void CalculateMultiplicativeEffects()
        {

        }

        /// <summary> Calculates the ki reductive effects. </summary>
        public void CalculateReductiveEffects()
        {

        }

        /// <summary> Creates total ki contribution. </summary>
        public void CreateTotalKiContribution(Dictionary<string, double> multiplicativeResultDictionary, double totalReductiveFactor)
        {
            MultiplicativeResultDictionary = multiplicativeResultDictionary;

            if (totalReductiveFactor <= 1)
            {
                totalReductiveFactor = 1.0D;
            }

            var dictionaryCount = MultiplicativeResultDictionary.Count();

            // for debugging terminals
            if (dictionaryCount > 3)
            {

            }

            TotalReductiveFactorOnStructure = totalReductiveFactor;

            foreach (double formulaValue in MultiplicativeResultDictionary.Values)
            {
                TotalMultiplicativeKiOnStructure *= formulaValue;
            }

            TotalKiContribution = TotalMultiplicativeKiOnStructure / TotalReductiveFactorOnStructure;


            //// K_i_numerator = (K_i (Air_Terminal) * FIR * K_i (Structure_@h_at ) * (multiplicative effects) / (R_f (Higher_structure_on_Lower_Structure)*R_f (Higher_structure_on_AT))
            //ki_numerator = (KiForPoi * FirAtPoi * KiForStructureAtPoi * TotalMultiplicativeKiOnStructure);

            //// K_i_denominator = (R_f (Higher_structure_on_Lower_Structure) * R_f (Higher_structure_on_AT))
            //var ki_denominator = TotalReductiveFactorOnStructure * TotalReductiveFactorOnDynasphere;
            //// The denominator cannot be less than 1 or else it will be a multiplicative factor.
            //ki_denominator = ki_denominator < 1 ? 1 : ki_denominator;

            //TotalKiContribution = ki_numerator / ki_denominator;
        }
    }

    #endregion Ki Data Transfer Object
}