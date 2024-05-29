// Copyright (c) 2022 Applied Software Technology, Inc.

using nVentErico.LPSD.Controllers.Cvm;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace nVentErico.LPSD.Controllers.Cvm
{
    /// <summary> The ki value calculation engine. </summary>
    public class KiEngine
    {
        #region Member Properties

        /// <summary> Gets or sets the web cookie from the CVM Controller. </summary>
        public dynamic UserCookie { get; set; }

        /// <summary> Gets or sets the current dynasphere being evaluated. </summary>
        public Terminal Terminal { get; set; }

        /// <summary> Gets or sets the current edge or corner point being evaluated. </summary>
        public Point Point { get; set; }

        /// <summary> The current building (structure) being evaluated. </summary>
        public Building CurrentBuilding { get; set; }

        /// <summary> List of Other buildings in the Forge Project. </summary>
        public List<Building> OtherBuildings { get; set; } = new List<Building>();

        /// <summary> Gets or sets the structure's level the dynasphere resides on. </summary>
        public Level CurrentLevel { get; set; }

        /// <summary> Gets or sets the structure's level the corner or edge point resides on. </summary>
        public Level LevelOfPoint { get; set; }

        /// <summary> Gets or sets the base level of building. </summary>
        public Level BaseLevelOfBuilding { get; set; }

        /// <summary> Gets or sets the POI location on the level. Corner, Edge or Middle. </summary>
        public PoiLocation PoiLocationOnLevel { get; set; }

        /// <summary> Gets or sets the poi point on location below. </summary>
        public PoiLocation PoiPointOnLocationBelow { get; set; }

        /// <summary> Gets or sets the shape of level the dynasphere resides on. </summary>
        public LevelShape ShapeOfPOILevel { get; set; }

        /// <summary> Gets or sets the type of the ki calculation. General, Multiplicative or Reductive. </summary>
        public KiCalculationType KiCalculationType { get; set; }

        /// <summary> LPL for the current Dynasphere. </summary>
        public int LightningProtectionLevel { get; set; }

        /// <summary> Default Values: </summary>
        public double H_Site { get; set; } = 0.0D;

        /// <summary> BreakDown E Field Constant E_o. </summary>
        public double BreakDownE_Field { get; private set; }

        /// <summary> Gets or sets the gable pitch value. </summary>
        public double GablePitch { get; set; }

        /// <summary> Gets or sets a value indicating whether this engine is evaluating a dynasphere. </summary>
        public bool EvaluatingDynasphere { get; set; } = false;

        /// <summary> Gets or sets a value indicating whether this engine is evaluating a point. </summary>
        public bool EvaluatingPoint { get; set; } = false;

        /// <summary>
        /// In meters: this may represent the elevation of the bolt origin which is likely the center of the storm cell:
        /// approx. 16,400 feet.
        /// </summary>
        public double CloudBase { get; set; } = 5000.0;

        /// <summary> Default discharge. </summary>
        public double Charge { get; set; } = 0.93;

        /// <summary> Gets or sets the velocity ratio. </summary>
        public double VelocityRatio { get; set; } = 1.1;

        /// <summary> Gets or sets the electrical epsilon. </summary>
        public double ElectricalEpsilon { get; set; } = 8.854188e-12;

        /// <summary> Gets or sets a value indicating whether the terminal is on mast. </summary>
        public bool DynasphereHigherThanFourMeters { get; set; } = false;

        /// <summary> default height for terminals - set when initial terminal selection is made. </summary>
        public double DefaultDynasphereHeight = 4.0;

        /// <summary> Gets or sets a dictionary of results. </summary>
        public Dictionary<string, double> ResultDictionary { get; set; } = new Dictionary<string, double>();

        /// <summary> Gets or sets the reductive ki for poi. </summary>
        public double ReductiveKiForPoi { get; set; } = 1.0D;

        #endregion Member Properties

        #region Constructors

        /// <summary> Constructor. </summary>
        ///
        /// <param name="formulaLetters"> The formula letters. </param>
        /// <param name="site"> The site. </param>
        /// <param name="building"> The current building (structure). </param>
        /// <param name="baseLevelOfBuilding"> The base level of building. </param>
        /// <param name="poiPoint"> (Optional) The poi point. </param>
        /// <param name="terminal"> (Optional) The current dynasphere being evaluated. </param>
        /// <param name="userCookie"> (Optional) The web cookie from the CVM Controller. </param>
        ///
        /// ### <param name="level"> The level. </param>
        public KiEngine(List<string> formulaLetters, Site site, Building building, Level baseLevelOfBuilding, List<Level> levelsOtherBldgs = null, Point poiPoint = null, Terminal terminal = null, dynamic userCookie = null)
        {
            UserCookie = userCookie;
            H_Site = Convert.ToDouble(site.SiteElevation);
            CurrentBuilding = building;
            BaseLevelOfBuilding = baseLevelOfBuilding;
            Point = poiPoint;
            Terminal = terminal;

            //GablePitch = level.GabelPitch;
            //Point.Level = level;
            //LevelOfPoint = level;

            // Multiplicative 
            InitFormulas(formulaLetters);

            // Get total Ki for points
            if (terminal == null && poiPoint != null)
            {
                poiPoint.KiData = new KiDto();

                // it is assumed that points have a LPL of 1;
                poiPoint.Q_LeaderCharge = 0.16;

                var totalReductiveFactor = 1.0D;

                // Get Reductive Ki
                if (poiPoint.Level.LevelsAbove.Count > 0 || levelsOtherBldgs.Count > 0)
                {
                    var thisLevel = poiPoint.Level;
                    var thisBldgLevelsAbove = building.Levels.Where(l => l.ForgeLevelElevation > thisLevel.ForgeLevelElevation).Select(l => l).ToList();



                    totalReductiveFactor = GetReductiveKiFactorFromLevels(poi: poiPoint,
                                                                          thisBldgLevelsAbove: thisBldgLevelsAbove,
                                                                          otherBldgsLevelsAbove: levelsOtherBldgs);

                }

                poiPoint.KiData.CreateTotalKiContribution(ResultDictionary, totalReductiveFactor);
            }

            // Get total Ki for terminals
            if (terminal != null)
            {
                terminal.KiData = new KiDto();

                var totalReductiveFactor = 1.0D;

                // Get Reductive Ki
                if (terminal.PoiPoint.Level.LevelsAbove.Count > 0)
                {
                    var thisLevel = terminal.PoiPoint.Level;
                    var thisBldgLevelsAbove = building.Levels.Where(l => l.ForgeLevelElevation > thisLevel.ForgeLevelElevation).Select(l => l).ToList();

                    if (thisBldgLevelsAbove.Count > 0)
                    {
                        totalReductiveFactor = GetReductiveKiFactorFromLevels(poi: terminal.PoiPoint,
                                                                              thisBldgLevelsAbove: thisBldgLevelsAbove,
                                                                              otherBldgsLevelsAbove: levelsOtherBldgs);
                    }
                }

                terminal.KiData.CreateTotalKiContribution(ResultDictionary, totalReductiveFactor);
            }
        }

        #endregion Constructor

        /// <summary> Initializes the formulas. </summary>
        ///
        /// <param name="formulaLetters"> The formula letters. </param>
        public void InitFormulas(List<string> formulaLetters)
        {
            double H = default(double);
            foreach (var formulaLetter in formulaLetters)
            {
                switch (formulaLetter)
                {
                    case ("A"):
                        Formula_A();
                        break;
                    case ("B"):
                        Formula_B();
                        break;
                    case ("C"):
                        break;
                    case ("D"):
                        Formula_D();
                        break;
                    case ("E"):
                        break;
                    case ("F"):
                        Formula_F();
                        break;
                    case ("G"):
                        Formula_G();
                        break;
                    case ("H"):
                        Formula_H();
                        break;
                    case ("I"):
                        break;
                    case ("J"):
                        Formula_J();
                        break;
                    case ("J5"):
                        Formula_J5();
                        break;
                    case ("K"):
                        Formula_K();
                        break;
                    case ("K5"):
                        Formula_K5();
                        break;
                    case ("L"):
                        Formula_L();
                        break;
                    case ("L5"):
                        Formula_L5();
                        break;
                    case ("M"):
                        Formula_M();
                        break;
                    case ("M5"):
                        Formula_M5();
                        break;
                    case ("N"):
                        Formula_N();
                        break;
                    case ("N5"):
                        Formula_N5();
                        break;
                    case ("O"):
                        Formula_O();
                        break;
                    case ("P"):
                        Formula_P();
                        break;
                    case ("Q"):
                        H = Point.Level.ForgeLevelElevation;
                        if (((0.1 * H) + 1.2) > 1.8)
                        {
                            ResultDictionary.Add("Q", 1.8);
                        }
                        else
                        {
                            ResultDictionary.Add("Q", (0.1 * H) + 1.2);
                        }
                        break;
                    case ("R"):
                        ResultDictionary.Add("R", 1.4);
                        break;
                    case ("S"):
                        H = Point.Level.ForgeLevelElevation;
                        if ((1.35 - (0.2 * H)) < 0.9)
                        {
                            ResultDictionary.Add("S", 0.9);
                        }
                        else
                        {
                            ResultDictionary.Add("S", (1.35 - (0.2 * H)));
                        }
                        break;
                    case ("T"):
                        ResultDictionary.Add("T", 1.5);
                        break;
                    case ("U"):
                        Formula_U();
                        break;
                    case ("V"):
                        Formula_V();
                        break;
                    case ("W"):
                        Formula_W();
                        break;
                    case ("X"):
                        Formula_X();
                        break;
                    case ("Y"):
                        Formula_Y();
                        break;
                    case ("Z"):
                        Formula_Z();
                        break;
                    default:
                        break;
                }
            }
        }

        /// <summary> Method to return value from Formula A. </summary>
        private void Formula_A()
        {
            // R_c is the critical radius
            double  R_c = 0.05D;

            double H = default(double); 
            double W = default(double); 
            double ki = default(double); 

            if (Point.IsExtendedCornerOrEdge | (Point.Level.LevelNumber == BaseLevelOfBuilding.LevelNumber))
            {
                H = Point.Level.ForgeLevelElevation;
                W = BaseLevelOfBuilding.BoundingBox.MinimumWidth;
            }
            else
            {
                H = Point.Level.ForgeLevelElevation - BaseLevelOfBuilding.ForgeLevelElevation;
                W = Point.Level.BoundingBox.MinimumWidth;
            }

            // K_i = 0.43H ^ (0.8) W ^ (-0.14)〖R_c〗^(-0.57) + 1
            ki = (0.43 * (Math.Pow(H, 0.8) * Math.Pow(W, -0.14) * Math.Pow(R_c, -0.57))) + 1;

            ki = Double.IsInfinity(ki) ? 1.0D : ki;

            if (!ResultDictionary.Keys.Contains("A"))
            {
                ResultDictionary.Add("A", ki);
            }
        }

        /// <summary> Method to return value from Formula B. </summary>
        private void Formula_B()
        {
            // R_c is the critical radius (0.05m for POIs)
            double  R_c = 0.05D;

            double H = default(double); 
            double W = default(double); 
            double ki = default(double); 

            if (Point.IsExtendedCornerOrEdge | (Point.Level.LevelNumber == BaseLevelOfBuilding.LevelNumber))
            {
                H = Point.Level.ForgeLevelElevation;
                W = BaseLevelOfBuilding.MinimumWidth;
            }
            else
            {
                H = Point.Level.ForgeLevelElevation - BaseLevelOfBuilding.ForgeLevelElevation;
                W = Point.Level.MinimumWidth;
            }
            
            // K_imin = 0.55H^0.544  W^(-0.14) R_c^(-0.367) + 1 
            var ki = (0.55 * Math.Pow(H, 0.544) * Math.Pow(W, -0.14) * Math.Pow(R_c, -0.367) + 1);

            ki = Double.IsInfinity(ki) ? 1.0D : ki;

            if (!ResultDictionary.Keys.Contains("B"))
            {
                ResultDictionary.Add("B", ki);
            }
        }

        /// <summary> Formula C (Surface horizontal only) </summary>

        /// <summary> Formula D. </summary>
        private void Formula_D()
        {
            // R_c is the critical radius (0.05m for POIs)
            double  R_c = 0.05D;

            double H = default(double); 
            double W = default(double); 
            double ki = default(double); 

            if (Point.Level.LevelNumber == BaseLevelOfBuilding.LevelNumber)
            {
                H = Point.Level.ForgeLevelElevation;
                W = BaseLevelOfBuilding.BoundingBox.MinimumWidth;
            }
            else
            {
                H = Point.Level.ForgeLevelElevation - BaseLevelOfBuilding.ForgeLevelElevation;
                W = Point.Level.BoundingBox.MinimumWidth;
            }

            //K_i at Structure = 0.56H^(0.82 ) W^(-0.31) 〖R_c〗^(-0.45) + 1 
            ki = 0.56 * (Mat.Pow(H, 0.82) * Math.Pow(W, -0.31) * Math.Pow(R_c, -0.45)) + 1;

            ki = Double.IsInfinity(ki) ? 1.0D : ki;

            if (!ResultDictionary.Keys.Contains("D"))
            {
                ResultDictionary.Add("D", ki);
            }
        }

        /// <summary> Formula F. </summary>
        private void Formula_F()
        {
            // R_c is the critical radius (0.05m for POIs)
            double  R_c = 0.05D;

            double H = default(double); 
            double W = default(double); 
            double ki = default(double); 

            // 𝑃 is the pitch of the gable roof
            double P = default(double);

            // -height 𝐻 to use is: 𝐻= ℎ / (𝑃𝛼+1)
            var pointLevelAboveBase = Point.Level.ForgeLevelElevation - BaseLevelOfBuilding.ForgeLevelElevation;
            P = Point.Slope;
            W = BaseLevelOfBuilding.BoundingBox.MinimumWidth;
            if (Point.IsExtendedCornerOrEdge)
            {
                H = Point.Position.Z;
            }
            else
            {
                H = Point.Position.Z - BaseLevelOfBuilding.ForgeLevelElevation;
            }

            double K_iMax = 1.0D;
            double K_iMin = 1.0D;

            // K_imax = 0.47〖(𝐻+𝑊)〗^0.76 𝑊^(−0.1) R_c^(−0.61) + 1
            K_iMax = (0.47 * Math.Pow(H + W, 0.76) * Math.Pow(W, -0.1) * Math.Pow(R_c, -0.61)) + 1;

            // 𝐾_𝑖min = 0.55 𝐻^0.544 𝑊^(−0.14) R_c^(−0.367) + 1
            K_iMin = (0.55 * System.Math.Pow(H, 0.544) * System.Math.Pow(W, -0.14) * System.Math.Pow(R_c, -0.367) + 1);

            // K_i = ((K_imax-K_imin)/2)P + K_imin
            ki = ((K_iMax - K_iMin) / 2) * P + K_iMin;

            ki = Double.IsInfinity(ki) ? 1.0D : ki;

            if (!ResultDictionary.Keys.Contains("F"))
            {
                ResultDictionary.Add("F", ki);
            }
        }

        /// <summary> Formula G. </summary>
        private void Formula_G()
        {
            // R_c is the critical radius (0.05m for POIs)
            double  R_c = 0.05D;

            double H = default(double); 
            double W = default(double); 
            double ki = default(double); 

            // 𝑃 is the pitch of the gable roof
            double P = default(double);

            // -height 𝐻 to use is: 𝐻= ℎ / (𝑃𝛼+1)
            var pointLevelAboveBase = Point.Level.ForgeLevelElevation - BaseLevelOfBuilding.ForgeLevelElevation;
            P = Point.Slope;
            W = BaseLevelOfBuilding.BoundingBox.MinimumWidth;

            if (Point.IsExtendedCornerOrEdge)
            {
                H = Point.Position.Z;
            }
            else
            {
                H = Point.Position.Z - BaseLevelOfBuilding.ForgeLevelElevation;
            }

            double K_iMax = 1.0D;
            double K_iMin = 1.0D;

            // Old 𝐾_𝑖𝑚𝑎𝑥 Formula found in PPX File Slide 24
            // 𝐾_𝑖𝑚𝑎𝑥 = 0.72〖(𝐻+𝑊)〗^0.51 𝑊^(−0.034) 𝐻_𝑓^(−0.45) + 0.34   MAX
            //K_iMax = 0.72 * (Math.Pow(H + W, 0.76) * Math.Pow(W, -0.034) * Math.Pow(h_f, -0.45)) + 0.34;

            // 𝐾_𝑖𝑚𝑎𝑥 = 0.48〖(𝐻+𝑊)〗^0.568 𝑊^(−0.037) R_c^(−0.508) + 1   MAX
            K_iMax = 0.48 * (Math.Pow(H + W, 0.568) * Math.Pow(W, -0.037) * Math.Pow(R_c, -0.508)) + 1;

            // Old 𝐾_𝑖𝑚𝑖𝑛 Formula found in PPX File Slide 24
            // 𝐾_𝑖𝑚𝑖𝑛 = 0.95〖(𝐻/𝑊)〗^0.57 𝑒^(−0.55〖(𝐻_𝑓/𝑊)〗^1.33 ) + 1	MIN
            //K_iMin = 0.95 * Math.Pow((H / W), 0.57) * Math.Exp(-0.55 * Math.Pow(h_f / W, 1.33)) + 1;

            // 𝐾_𝑖𝑚𝑖𝑛 = 0.95〖(𝐻/𝑊)〗^0.57 + 1	MIN
            K_iMin = 0.95 * Math.Pow((H / W), 0.57) + 1;

            // K_i = ((K_imax-K_imin)/2)P + K_imin
            ki = ((K_iMax - K_iMin) / 2) * P + K_iMin;

            ki = Double.IsInfinity(ki) ? 1.0D : ki;

            if (!ResultDictionary.Keys.Contains("G"))
            {
                ResultDictionary.Add("G", ki);
            }
        }

        /// <summary> Method to return value from Formula H. </summary>
        private void Formula_H()
        {
            // ℎ_𝑎𝑡 is the height of the dynasphere above its level
            var h_at = Terminal.HeightAboveStructure;

            // r_d is the dynasphere radius (0.175 meters)
            var r_d = 0.175D;

            // K_i at dynasphere = (1.4〖(h_at/r_d )〗^0.87 + 1)
            var kiAtDynasphere = (1.4 * Math.Pow((h_at / r_d), 0.87) + 1);

            if (!ResultDictionary.Keys.Contains("H"))
            {
                ResultDictionary.Add("H", kiAtDynasphere);
            }
        }

        /// <summary> Method to return value from Formula I. </summary>
        private void Formula_I()
        {
            // ℎ_𝑎𝑡 is the height of the air terminal above its level
            var h_at = Terminal.HeightAboveStructure;

            // R_c is the critical radius of generic terminals (0.38 meters)
            var R_c = 0.38D;

            // K_i at air terminal = (1.4〖(h_at/r_d )〗^0.87 + 1)
            var kiAtDynasphere = (1.4 * Math.Pow((h_at / R_c), 0.87) + 1);

            if (!ResultDictionary.Keys.Contains("I"))
            {
                ResultDictionary.Add("I", kiAtDynasphere);
            }
        }

        /// <summary> Method to return value from Formula J. </summary>
        private void Formula_J()
        {
            double H_f = default(double);
            double H = default(double); 
            double W = default(double); 
            double ki = default(double); 

            if (Terminal.Level.LevelNumber == BaseLevelOfBuilding.LevelNumber)
            {
                H = BaseLevelOfBuilding.ForgeLevelElevation;
                W = BaseLevelOfBuilding.BoundingBox.MinimumWidth;
                H_f = Point.Position.Z - BaseLevelOfBuilding.ForgeLevelElevation;
            }
            if (Terminal.PoiPoint.IsExtendedCornerOrEdge)
            {
                H = Terminal.Level.ForgeLevelElevation;
                W = BaseLevelOfBuilding.BoundingBox.MinimumWidth;
                H_f = Terminal.HeightAboveStructure;
            }
            
            // K_i at base structure = 0.57H^(0.75) W^(-0.13) 〖H_f〗^(-0.53) + 0.4
            ki = 0.57 * Math.Pow(H, 0.75) * Math.Pow(W, -0.13) * Math.Pow(H_f, -0.53) + 0.4;

            ki = Double.IsInfinity(ki) ? 1.0D : ki;

            if (!ResultDictionary.Keys.Contains("J"))
            {
                ResultDictionary.Add("J", ki);
            }
        }

        /// <summary> Method to return value from Formula K. </summary>
        private void Formula_K()
        {
            double H_f = default(double);
            double H = default(double); 
            double W = default(double); 
            double ki = default(double); 

            if (Terminal.Level.LevelNumber == BaseLevelOfBuilding.LevelNumber)
            {
                H = BaseLevelOfBuilding.ForgeLevelElevation;
                W = BaseLevelOfBuilding.BoundingBox.MinimumWidth;
                H_f = Point.Position.Z - BaseLevelOfBuilding.ForgeLevelElevation;
            }
            if (Terminal.PoiPoint.IsExtendedCornerOrEdge)
            {
                H = Terminal.Level.ForgeLevelElevation;
                W = BaseLevelOfBuilding.BoundingBox.MinimumWidth;
                H_f = Terminal.HeightAboveStructure;
            }

            //// K_i at base structure = Ki = 0.84 * 𝐻^0.474 * 𝑊^(−0.109) * 𝐻_𝑓^(−0.326) + 0.27
            var ki = 0.84 * Math.Pow(H, 0.474) * Math.Pow(W, -0.109) * Math.Pow(H_f, -0.326) + 0.27;

            ki = Double.IsInfinity(ki) ? 1.0D : ki;

            if (!ResultDictionary.Keys.Contains("K"))
            {
                ResultDictionary.Add("K", ki);
            }
        }

        /// <summary> Formula J 5. </summary>
        private void Formula_J5()
        {
            var H_f = Terminal.HeightAboveStructure;
            var H = Terminal.Level.ForgeLevelElevation - BaseLevelOfBuilding.ForgeLevelElevation;
            var W = Terminal.Level.MinimumWidth;

            // K_i at base structure = 0.57H^(0.75) W^(-0.13) 〖H_f〗^(-0.53) + 0.4
            var ki = 0.57 * Math.Pow(H, 0.75) * Math.Pow(W, -0.13) * Math.Pow(H_f, -0.53) + 0.4;

            ki = Double.IsInfinity(ki) ? 1.0D : ki;

            if (!ResultDictionary.Keys.Contains("J5"))
            {
                ResultDictionary.Add("J5", ki);
            }
        }

        /// <summary> Formula K 5. </summary>
        private void Formula_K5()
        {
            var H_f = Terminal.Top.Z - Terminal.Level.ForgeLevelElevation;
            var H = Terminal.Level.ForgeLevelElevation - BaseLevelOfBuilding.ForgeLevelElevation;
            var W = BaseLevelOfBuilding.BoundingBox.MinimumWidth;

            // K_i at base structure = Ki = 0.84 * 𝐻^0.474 * 𝑊^(−0.109) * 𝐻_𝑓^(−0.326) + 0.27
            var ki = 0.84 * Math.Pow((H), 0.474) * Math.Pow(W, -0.109) * Math.Pow(H_f, -0.326) + 0.27;

            ki = Double.IsInfinity(ki) ? 1.0D : ki;

            if (!ResultDictionary.Keys.Contains("K5"))
            {
                ResultDictionary.Add("K5", ki);
            }
        }

        /// <summary> Formula L 5. </summary>
        private void Formula_L5()
        {
            var H_f = Terminal.Top.Z - Terminal.Level.ForgeLevelElevation;
            var H = Terminal.Level.ForgeLevelElevation - BaseLevelOfBuilding.ForgeLevelElevation;
            var W = Terminal.Level.MinimumWidth;

            // (0.95 * 𝐻^0.57 * W^-0.57 * e^-0.55*(H_f/W)^1.33) + 1
            var ki = 0.95 * Math.Pow(H, 0.57) * Math.Pow(W, -0.57) * Math.Exp(-0.55 * Math.Pow((H_f) / W, 1.33)) + 1;

            ki = Double.IsInfinity(ki) ? 1.0D : ki;

            if (!ResultDictionary.Keys.Contains("L5"))
            {
                ResultDictionary.Add("L5", ki);
            }
        }

        /// <summary> Formula L. </summary>
        private void Formula_L()
        {
            double ki;
            var H = BaseLevelOfBuilding.ForgeLevelElevation;
            var W = BaseLevelOfBuilding.BoundingBox.MinimumWidth;

            if (Terminal != null)
            {
                var H_f = Terminal.Top.Z - BaseLevelOfBuilding.ForgeLevelElevation;
            }
            else
            {
                var H_f = Point.Position.Z - BaseLevelOfBuilding.ForgeLevelElevation;
            }

            // (0.95 * (H/W)^0.57 * e^(-0.55(H_f/W)^1.33) + 1
            ki = 0.95 * Math.Pow((H / W), 0.57) * Math.Exp(-0.55 * Math.Pow(H_f / W, 1.33)) + 1;

            ki = Double.IsInfinity(ki) ? 1.0D : ki;

            ResultDictionary.Add("L", ki);
        }

        /// <summary> Formula M. </summary>
        private void Formula_M()
        {
            double ki = 1;

            if (Terminal.Level.LevelNumber == BaseLevelOfBuilding.LevelNumber)
            {
                var H_f = Terminal.Top.Z - BaseLevelOfBuilding.ForgeLevelElevation;
                var H = BaseLevelOfBuilding.ForgeLevelElevation;
                var W = Terminal.Level.BoundingBox.MinimumWidth;
            }
            else
            {
                var H_f = Terminal.Top.Z - Terminal.Level.ForgeLevelElevation;
                var H = Terminal.Level.ForgeLevelElevation - BaseLevelOfBuilding.ForgeLevelElevation;
                var W = Terminal.Level.BoundingBox.MinimumWidth;
            }

            // K_i at Structure = 0.68 𝐻^0.78 𝑊^(−0.28) 𝐻_𝑓^(−0.43) + 0.45
            ki = 0.68 * Math.Pow(H, 0.78) * Math.Pow(W, -0.28) * Math.Pow(H_f, -0.43) + 0.45;

            ki = Double.IsInfinity(ki) ? 1.0D : ki;

            if (!ResultDictionary.Keys.Contains("M"))
            {
                ResultDictionary.Add("M", ki);
            }
        }

        /// <summary> Formula M5. </summary>
        private void Formula_M5()
        {
            double ki;

            var H_f = Terminal.Top.Z - Terminal.Level.ForgeLevelElevation;
            var H = Terminal.Level.ForgeLevelElevation - BaseLevelOfBuilding.ForgeLevelElevation;
            var W = Terminal.Level.BoundingBox.MinimumWidth;

            // K_i at Structure = 0.68 𝐻^0.78 𝑊^(−0.28) 𝐻_𝑓^(−0.43) + 0.45
            ki = 0.68 * Math.Pow(H, 0.78) * Math.Pow(W, -0.28) * Math.Pow(H_f, -0.43) + 0.45;

            ki = Double.IsInfinity(ki) ? 1.0D : ki;

            if (!ResultDictionary.Keys.Contains("M5"))
            {
                ResultDictionary.Add("M5", ki);
            }
        }

        /// <summary> Formula N. </summary>
        private void Formula_N()
        {
            double ki;

            if (Terminal != null)
            {
                var H_f = Terminal.Top.Z - BaseLevelOfBuilding.ForgeLevelElevation;
            }
            else
            {
                var H_f = Point.Position.Z - BaseLevelOfBuilding.ForgeLevelElevation;
            }

            var W = BaseLevelOfBuilding.BoundingBox.MinimumWidth;
            var H = BaseLevelOfBuilding.ForgeLevelElevation;

            // K_i = 1.375(H/W)^0.839 e^(-1.33 * (H_f/W)^1.43) + 1
            ki = (1.375 * Math.Pow(H / W, 0.839) * Math.Exp(-1.33 * Math.Pow(H_f / W, 1.43)) + 1);

            ki = Double.IsInfinity(ki) ? 1.0D : ki;

            if (!ResultDictionary.Keys.Contains("N"))
            {
                ResultDictionary.Add("N", ki);
            }
        }

        /// <summary> Formula N5. </summary>
        private void Formula_N5()
        {
            var H_f = Terminal.Top.Z - Terminal.Level.ForgeLevelElevation;
            var W = BaseLevelOfBuilding.BoundingBox.MinimumWidth;
            var H = BaseLevelOfBuilding.ForgeLevelElevation;

            // K_i = 1.375(H/W)^0.839 e^(-1.33) (H_f/W)^1.43 + 1
            var ki = (1.375 * Math.Pow(H / W, 0.839) * Math.Exp(-1.33 * Math.Pow(H_f / W, 1.43)) + 1);

            ki = Double.IsInfinity(ki) ? 1.0D : ki;

            if (!ResultDictionary.Keys.Contains("N5"))
            {
                ResultDictionary.Add("N5", ki);
            }
        }

        /// <summary> Method to return value from Formula O. </summary>
        private void Formula_O()
        {
            if ((Terminal.Level.LevelNumber == BaseLevelOfBuilding.LevelNumber) | Terminal.IsExtendedCornerOrEdge)
            {
                var H_f = Terminal.Top.Z - Terminal.Level.ForgeLevelElevation;
                var W = Terminal.Level.BoundingBox.MinimumWidth;
                var H = Terminal.Level.ForgeLevelElevation;
            }
            else
            {
                var H_f = Terminal.Top.Z - Terminal.Level.ForgeLevelElevation;
                var W = Terminal.Level.BoundingBox.MinimumWidth;
                var H = Terminal.Level.ForgeLevelElevation - BaseLevelOfBuilding.ForgeLevelElevation;
            }

            P = Terminal.PoiPoint.Slope;            

            double ki = 1.0D;
            double K_iMax = 1.0D;
            double K_iMin = 1.0D;

            // K_imax = 〖(𝐻+𝑊)〗^0.63 𝑊^(−0.1) 𝐻_𝑓^(−0.49) − 1
            K_iMax = Math.Pow(H + W, 0.63) * Math.Pow(W, -0.1) * Math.Pow(H_f, -0.49) + 1;

            // 𝐾_𝑖min = 0.84 𝐻^0.474 𝑊^(−0.109) 𝐻_𝑓^(−0.326) + 0.27
            K_iMin = (0.84 * System.Math.Pow(H, 0.474) * System.Math.Pow(W, -0.109) * System.Math.Pow(H_f, -0.326) + 0.27);

            // K_i = ((K_imax-K_imin)/2)P + K_imin
            ki = ((K_iMax - K_iMin) / 2) * P + K_iMin;

            ki = Double.IsInfinity(ki) ? 1.0D : ki;

            if (!ResultDictionary.Keys.Contains("O"))
            {
                ResultDictionary.Add("O", ki);
            }
        }

        /// <summary> Method to return value from Formula P. </summary>
        private void Formula_P()
        {
            if ((Terminal.Level.LevelNumber == BaseLevelOfBuilding.LevelNumber) | Terminal.IsExtendedCornerOrEdge)
            {
                var H_f = Terminal.Top.Z - Terminal.Level.ForgeLevelElevation;
                var W = Terminal.Level.BoundingBox.MinimumWidth;
                var H = Terminal.Level.ForgeLevelElevation;
            }
            else
            {
                var H_f = Terminal.Top.Z - Terminal.Level.ForgeLevelElevation;
                var W = Terminal.Level.BoundingBox.MinimumWidth;
                var H = Terminal.Level.ForgeLevelElevation - BaseLevelOfBuilding.ForgeLevelElevation;
            }

            P = Terminal.PoiPoint.Slope;            

            double ki = 1.0D;
            double K_iMax = 1.0D;
            double K_iMin = 1.0D;

            // 𝐾_𝑖𝑚𝑎𝑥 = 0.72〖(𝐻+𝑊)〗^0.51 𝑊^(−0.034) 𝐻_𝑓^(−0.45) + 0.34   MAX
            K_iMax = 0.72 * (Math.Pow(H + W, 0.76) * Math.Pow(W, -0.034) * Math.Pow(H_f, -0.45)) + 0.34;

            // 𝐾_𝑖𝑚𝑖𝑛 = 0.95〖(𝐻/𝑊)〗^0.57 𝑒^(−0.55〖(𝐻_𝑓/𝑊)〗^1.33 ) + 1	MIN
            K_iMin = 0.95 * Math.Pow((H / W), 0.57) * Math.Exp(-0.55 * Math.Pow(H_f / W, 1.33)) + 1;

            // K_i = ((K_imax-K_imin)/2)P + K_imin
            ki = ((K_iMax - K_iMin) / 2) * P + K_iMin;

            ki = Double.IsInfinity(ki) ? 1.0D : ki;

            if (!ResultDictionary.Keys.Contains("P"))
            {
                ResultDictionary.Add("P", ki);
            }
        }

        /// <summary> Method to return value from Formula U. </summary>
        private void Formula_U()
        {
            double FIR;
            double H;
            double W;

            if (Terminal.Level.LevelNumber == BaseLevelOfBuilding.LevelNumber)
            {
                H = BaseLevelOfBuilding.ForgeLevelElevation;
                W = BaseLevelOfBuilding.BoundingBox.MinimumWidth;
            }
            else
            {
                if (Terminal.PoiPoint.IsExtendedCornerOrEdge)
                {
                    H = Terminal.Level.HeightJustThisLevel;
                    W = BaseLevelOfBuilding.BoundingBox.MinimumWidth;
                }
                else
                {
                    H = Terminal.Level.ForgeLevelElevation - BaseLevelOfBuilding.ForgeLevelElevation;
                    W = Terminal.Level.BoundingBox.MinimumWidth;
                }
            }

            // 𝐹𝐼𝑅 = 0.9𝐻^0.25 * 𝑊^(−0.13) + 0.2
            FIR = 0.9 * Math.Pow(H, 0.25) * Mat.Pow(W, -0.13) + 0.2;

            FIR = Double.IsInfinity(FIR) ? 1.0D : FIR;

            if (!ResultDictionary.Keys.Contains("U"))
            {
                ResultDictionary.Add("U", FIR);
            }
        }


        /// <summary> Method to return value from Formula V. </summary>
        private void Formula_V()
        {

            double FIR;
            double H;
            double W;

            if (Terminal.Level.LevelNumber == BaseLevelOfBuilding.LevelNumber)
            {
                H = BaseLevelOfBuilding.ForgeLevelElevation;
                W = BaseLevelOfBuilding.BoundingBox.MinimumWidth;
            }
            else
            {
                if (Terminal.PoiPoint.IsExtendedCornerOrEdge)
                {
                    H = Terminal.Level.HeightJustThisLevel;
                    W = BaseLevelOfBuilding.BoundingBox.MinimumWidth;
                }
                else
                {
                    H = Terminal.Level.ForgeLevelElevation - BaseLevelOfBuilding.ForgeLevelElevation;
                    W = Terminal.Level.BoundingBox.MinimumWidth;                    
                }
            }

            // 0.4 * (H^0.4) * (W^-0.3) + 0.7
            FIR = (0.4 * Math.Pow(H, 0.4) * Math.Pow(W, -0.3) + 0.7);

            FIR = Double.IsInfinity(FIR) ? 1.0D : FIR;

            if (!ResultDictionary.Keys.Contains("V"))
            {
                ResultDictionary.Add("V", FIR);
            }
        }

        /// <summary> Formula W. </summary>
        private void Formula_W()
        {
            double FIR;
            double H;
            double W;

            if (Terminal.Level.LevelNumber == BaseLevelOfBuilding.LevelNumber)
            {
                H = BaseLevelOfBuilding.ForgeLevelElevation;
                W = BaseLevelOfBuilding.BoundingBox.MinimumWidth;
            }
            else
            {
                if (Terminal.PoiPoint.IsExtendedCornerOrEdge)
                {
                    H = Terminal.Level.HeightJustThisLevel;
                    W = BaseLevelOfBuilding.BoundingBox.MinimumWidth;
                }
                else
                {
                    H = Terminal.Level.ForgeLevelElevation - BaseLevelOfBuilding.ForgeLevelElevation;
                    W = Terminal.Level.BoundingBox.MinimumWidth;
                }
            }

            // FIR = 0.5H^(-0.3) W^0.18 + 1
            FIR = (0.5 * Math.Pow(H, -0.3) * Math.Pow(W, 0.18) + 1);
            
            FIR = Double.IsInfinity(FIR) ? 1.0D : FIR;

            if (!ResultDictionary.Keys.Contains("W"))
            {
                ResultDictionary.Add("W", FIR);
            }
        }

        /// <summary> Method to return value from Formula X. </summary>
        private void Formula_X()
        {

            double FIR;
            double H;
            double W;

            if (Terminal.Level.LevelNumber == BaseLevelOfBuilding.LevelNumber)
            {
                H = BaseLevelOfBuilding.ForgeLevelElevation;
                W = BaseLevelOfBuilding.BoundingBox.MinimumWidth;
            }
            else
            {
                if (Terminal.PoiPoint.IsExtendedCornerOrEdge)
                {
                    H = Terminal.Level.HeightJustThisLevel;
                    W = BaseLevelOfBuilding.BoundingBox.MinimumWidth;                   
                }
                else
                {
                    H = Terminal.Level.ForgeLevelElevation - BaseLevelOfBuilding.ForgeLevelElevation;
                    W = Terminal.Level.BoundingBox.MinimumWidth;
                }
            }

            // FIR = 0.12 * H^0.4 *  W^(-0.6) + 1
            FIR = (0.12 * Math.Pow(H, 0.4) * Math.Pow(W, -0.6) + 1);

            FIR = Double.IsInfinity(FIR) ? 1.0D : FIR;

            if (!ResultDictionary.Keys.Contains("X"))
            {
                ResultDictionary.Add("X", FIR);
            }
        }

        private void Formula_Y()
        {
            if (Terminal.Level.LevelNumber == BaseLevelOfBuilding.LevelNumber)
            {
                var H = BaseLevelOfBuilding.ForgeLevelElevation;
                var W = BaseLevelOfBuilding.BoundingBox.MinimumWidth;
            }
            else
            {
                if (Terminal.PoiPoint.IsExtendedCornerOrEdge)
                {
                    var H = Terminal.Level.ForgeLevelElevation;
                    var W = BaseLevelOfBuilding.BoundingBox.MinimumWidth;
                }
                else
                {
                    var H = Terminal.Level.ForgeLevelElevation - BaseLevelOfBuilding.ForgeLevelElevation;
                    var W = BaseLevelOfBuilding.BoundingBox.MinimumWidth;            
                }
            }
            
            P = Terminal.PoiPoint.Slope;            

            double FIR = 1.0D;
            double Fir_Max = 1.0D;
            double Fir_Min = 1.0D;

            // 〖FIR〗_max=〖1.8(H+W)〗^(-0.12) + 1
            Fir_Max = 1.8 * Math.Pow(H + W, -0.12) + 1;

            //〖FIR〗_min = 0.9H ^ 0.25 W ^ (-0.13) + 0.2
            Fir_Min = 0.9 * Math.Pow(H, 0.25) * Math.Pow(W, -0.13) + 0.2;

            // FIR = ((〖FIR〗_max -〖FIR〗_min)/ 2)P +〖FIR〗_min
            FIR = ((Fir_Max - Fir_Min) / 2) * P + Fir_Min;

            FIR = Double.IsInfinity(FIR) ? 1.0D : FIR;

            if (!ResultDictionary.Keys.Contains("Y"))
            {
                ResultDictionary.Add("Y", FIR);
            }
        }

        private void Formula_Z()
        {
            if (Terminal.Level.LevelNumber == BaseLevelOfBuilding.LevelNumber)
            {
                var H = BaseLevelOfBuilding.ForgeLevelElevation;
                var W = BaseLevelOfBuilding.BoundingBox.MinimumWidth;
            }
            else
            {
                if (Terminal.PoiPoint.IsExtendedCornerOrEdge)
                {
                    var H = Terminal.Level.ForgeLevelElevation;
                    var W = BaseLevelOfBuilding.BoundingBox.MinimumWidth;
                }
                else
                {
                    var H = Terminal.Level.ForgeLevelElevation - BaseLevelOfBuilding.ForgeLevelElevation;
                    var W = BaseLevelOfBuilding.BoundingBox.MinimumWidth;            
                }
            }
            
            P = Terminal.PoiPoint.Slope;            

            double FIR = 1.0D;
            double Fir_Max = 1.0D;
            double Fir_Min = 1.0D;

            // 〖𝐹𝐼𝑅〗_𝑚𝑎𝑥 =〖0.55 (𝐻+𝑊)〗^0.4  𝑊^(−0.35) + 1
            Fir_Max = (0.55 * Math.Pow(H + W, 0.4)) * Math.Pow(W, -0.35) + 1;

            //〖〖𝐹𝐼𝑅〗_𝑚𝑖𝑛 = 0.4𝐻^0.4 𝑊^(−0.3)+0.7
            Fir_Min = 0.4 * Math.Pow(H, 0.4) * Math.Pow(W, -0.3) + 0.7;

            // FIR = ((〖FIR〗_max -〖FIR〗_min)/ 2)P +〖FIR〗_min
            FIR = ((Fir_Max - Fir_Min) / 2) * P + Fir_Min;

            FIR = Double.IsInfinity(FIR) ? 1.0D : FIR;

            if (!ResultDictionary.Keys.Contains("Z"))
            {
                ResultDictionary.Add("Z", FIR);
            }
        }

        /// <summary> Calculates the reductive factor on a POI. 
        ///           Features that are part of the same “virtual building” 
        ///           will check for reduction assuming they are composite structures 
        ///           without needing to calculate the minimum separation distance 
        ///           and interpolating the ultimate reduction factor.
        ///           Similarly, for structures of similar heights in the same general area 
        ///           can be grouped into the same “virtual building” 
        ///           as the reduction factor between one another will not yield a significant value to affect results 
        ///           (Rf will likely be less than 1 and thus rounded up to 1 which is the same as no reduction) </summary>
        ///
        /// <param name="poi"> The point number. </param>
        /// <param name="thisBldgLevelsAbove"> Levels above the POI on this building. </param>
        /// <param name="otherBldgsLevelsAbove"> (Optional) Levels above the POI on other buildings. </param>
        public double GetReductiveKiFactorFromLevels(Point poi, List<Level> thisBldgLevelsAbove = null, List<Level> otherBldgsLevelsAbove = null)
        {
            var magicPointsThisBldg = new List<Point>();
            var magicPointsOtherBldgs = new List<Point>();
            double R_f = 1.0D;

            var poiLevel = poi.Level;
            var minimumReductiveDistance = poiLevel.MinimumReductiveDistance;

            // Distance d between this POI's level to level above on another building
            double d_levelToLevelOnOtherBldg = 0.00D;

            try
            {
                if (thisBldgLevelsAbove != null)
                {
                    foreach (var levelAbove in thisBldgLevelsAbove)
                    {
                        var validPointsAbove = levelAbove.PointsByLevelGuid.Where(p => p.IsCorner ||
                                                                                       p.IsEdgeRectangular ||
                                                                                       p.IsEdgeOval ||
                                                                                       p.IsGableEaveCorner ||
                                                                                       p.IsGableRidgeCorner ||
                                                                                       p.IsGableEaveEdge ||
                                                                                       p.IsGableRidgeEdge ||
                                                                                       p.IsGableRoof).Select(p => p).ToList();
                        foreach (var pointAbove in validPointsAbove)
                        {
                            double distanceToPoint = GetHypotenuse2DFromPoint(referencePosition: poi.Position, pointPosition: pointAbove.Position);

                            // If the distance to the point being evaluated is less than the min distance:
                            // Then evaluate the point for reductive values
                            if (distanceToPoint < poi.Level.MinimumReductiveDistance)
                            {
                                var d_2D = Math.Sqrt(Math.Pow((poi.Position.X - pointAbove.Position.X), 2) + Math.Pow((poi.Position.Y - pointAbove.Position.Y), 2));
                                var H_P = pointAbove.Position.Z;
                                var W_P = levelAbove.MinimumWidth;

                                // Magic Number:
                                // 𝑀 = 1/(𝑑_2𝐷+1)∗〖𝐻_𝐶𝑃〗^0.8∗〖𝑊_𝐶𝑃〗^0.3
                                var magicNumber = (1 / (d_2D + 1)) * Math.Pow(H_P, 0.8) * Math.Pow(W_P, 0.3);

                                pointAbove.MagicNumber = magicNumber;

                                magicPointsThisBldg.Add(pointAbove);
                            }
                        }
                    }
                }

                if (otherBldgsLevelsAbove != null)
                {
                    // Determine if this building's level distance to other buildings' levels is greater than this level's MinimumReductiveDistance
                    // If so, eliminate them from the levels to evaluate
                    foreach (var levelOnOtherBuilding in otherBldgsLevelsAbove)
                    {
                        var validPointsAbove = levelOnOtherBuilding.PointsByLevelGuid.Where(p => p.IsCorner ||
                                                                                            p.IsEdgeRectangular ||
                                                                                            p.IsEdgeOval ||
                                                                                            p.IsGableEaveCorner ||
                                                                                            p.IsGableRidgeCorner ||
                                                                                            p.IsGableEaveEdge ||
                                                                                            p.IsGableRidgeEdge ||
                                                                                            p.IsGableRoof).Select(p => p).ToList();

                        foreach (var pointAbove in validPointsAbove)
                        {
                            double distanceToPoint = GetHypotenuse2DFromPoint(referencePosition: poi.Position, pointPosition: pointAbove.Position);

                            // If the distance to the point being evaluated is less than the min distance:
                            // Then evaluate the point for reductive values
                            if (distanceToPoint < poi.Level.MinimumReductiveDistance)
                            {
                                var d_2D = Math.Sqrt(Math.Pow((poi.Position.X - pointAbove.Position.X), 2) + Math.Pow((poi.Position.Y - pointAbove.Position.Y), 2));
                                var H_P = pointAbove.Position.Z;
                                var W_P = levelOnOtherBuilding.MinimumWidth;

                                // Magic Number:
                                // 𝑀 = 1/(𝑑_2𝐷+1)∗〖𝐻_𝐶𝑃〗^0.8∗〖𝑊_𝐶𝑃〗^0.3
                                var magicNumber = (1 / (d_2D + 1)) * Math.Pow(H_P, 0.8) * Math.Pow(W_P, 0.3);

                                pointAbove.MagicNumber = magicNumber;

                                magicPointsOtherBldgs.Add(pointAbove);
                            }
                        }
                    }
                }

                bool magicPointOnThisBuilding = false;
                Point magicPointThisBldg = new Point();
                double magicPointMaxThisBldg = 0.0D;
                Point magicPointOtherBldgs = new Point();
                double magicPointMaxOtherBldgs = 0.0D;

                if (magicPointsThisBldg.Count() > 0)
                {
                    List<double> magicPointValues = magicPointsThisBldg.Select(p => p.MagicNumber).ToList();
                    magicPointMaxThisBldg = magicPointValues.Max();
                    var maxValuePoints = magicPointsThisBldg.Where(p => p.MagicNumber == magicPointMaxThisBldg).ToList();
                    if (maxValuePoints.Count == 1)
                    {
                        magicPointThisBldg = maxValuePoints.First();
                    }
                }

                if (magicPointsOtherBldgs.Count() > 0)
                {
                    List<double> magicPointValues = magicPointsOtherBldgs.Select(p => p.MagicNumber).ToList();
                    magicPointMaxOtherBldgs = magicPointValues.Max();
                    var maxValuePoints = magicPointsOtherBldgs.Where(p => p.MagicNumber == magicPointMaxOtherBldgs).ToList();
                    if (maxValuePoints.Count == 1)
                    {
                        magicPointOtherBldgs = maxValuePoints.First();
                    }
                }

                if (magicPointMaxThisBldg > magicPointMaxOtherBldgs)
                {
                    magicPointOnThisBuilding = true;
                }
                else
                {
                    magicPointOnThisBuilding = false;
                }

                if (magicPointOnThisBuilding && magicPointThisBldg.Level != null && magicPointThisBldg.Position != null)
                {
                    var H_1 = magicPointThisBldg.Position.Z;
                    var H_2 = poi.Position.Z;

                    poi.MagicPoint = magicPointThisBldg;

                    var delta_Z = H_1 - H_2;

                    var d_2D = Math.Sqrt(Math.Pow((poi.Position.X - magicPointThisBldg.Position.X), 2) + Math.Pow((poi.Position.Y - magicPointThisBldg.Position.Y), 2));

                    // Magic Point Reduction calculation for Same Building
                    double R_ce = 1.00D;

                    if (!magicPointThisBldg.Level.IsSlender && delta_Z > 0 && d_2D != 0.00D)
                    {
                        var R_f1 = (0.9 * Math.Pow((delta_Z), 0.51));
                        var R_f2 = Math.Pow(d_2D, -0.35);

                        R_ce = (0.9 * Math.Pow((delta_Z), 0.51) * Math.Pow(d_2D, -0.35));

                        R_ce = Double.IsInfinity(R_ce) ? 1.0D : R_ce;

                        R_f = R_ce;
                    }
                    else
                    {
                        // reductive influence of a passive terminal on the structure
                    }
                }
                if (!magicPointOnThisBuilding && magicPointOtherBldgs.Level != null && magicPointOtherBldgs.Position != null)
                {
                    var H_1 = magicPointOtherBldgs.Position.Z;
                    var H_2 = poi.Position.Z;

                    poi.MagicPoint = magicPointOtherBldgs;

                    var delta_Z = H_1 - H_2;

                    double d_min = 3.8 * Math.Pow(poi.Position.Z, 0.78) * Math.Pow(poi.Level.MinimumWidth, 0.28) / 2;

                    var d_2D = Math.Sqrt(Math.Pow((poi.Position.X - magicPointOtherBldgs.Position.X), 2) + Math.Pow((poi.Position.Y - magicPointOtherBldgs.Position.Y), 2));

                    d_levelToLevelOnOtherBldg = GetDistanceBetweenLevels(poi.Level, magicPointOtherBldgs.Level);

                    double R_i = 1.00D;

                    if (delta_Z > 0 && d_2D != 0.00)
                    {
                        var R_f1 = (0.9 * Math.Pow((delta_Z), 0.51));
                        var R_f2 = Math.Pow(d_2D, -0.35);

                        double Rf_max = (0.9 * Math.Pow((delta_Z), 0.51) * Math.Pow(d_2D, -0.35));
                        double Rf_min = 1;

                        R_i = Rf_max - (d_2D * (Rf_max - 1) / d_min);

                        R_i = Double.IsInfinity(R_i) ? 1.0D : R_i;

                        R_f = R_i;
                    }
                }
            }
            catch (Exception)
            {
                throw;
            }

            if (R_f <= 1)
            {
                return 1.0D;
            }
            else
            {
                return R_f;
            }
        }

        /// <summary> Gets distance between levels. </summary>
        ///
        /// <param name="level"> The level. </param>
        /// <param name="levelOnOtherBuilding"> The level on other building. </param>
        private double GetDistanceBetweenLevels(Level level, Level levelOnOtherBuilding)
        {
            double distanceBetween = 1.0D;
            List<double> hullPointDistances = new List<double>();

            try
            {
                double tempD = 0.0D;

                foreach (threeVector3 thisLevelHullPoint in level.ConvexHullPoints)
                {
                    foreach (threeVector3 otherLevelHullPoint in levelOnOtherBuilding.ConvexHullPoints)
                    {
                        tempD = GetHypotenuse2DFrom3DVectorlPoints(referencePosition: thisLevelHullPoint, pointToEvaluate: otherLevelHullPoint);

                        if (tempD > level.MinimumReductiveDistance)
                        {
                            hullPointDistances.Add(tempD);
                        }
                    }
                }

                if (hullPointDistances.Count > 0)
                {
                    distanceBetween = hullPointDistances.Min();
                }
                else
                {
                    distanceBetween = 1.0D;
                }

            }
            catch (Exception ex)
            {

                throw ex;
            }

            return distanceBetween;
        }

        /// <summary> Gets the hypotenuse from 2D point to points. </summary>
        ///
        /// <exception cref="Exception"> Thrown when an exception error condition occurs. </exception>
        ///
        /// <param name="referencePosition"> The terminal location. </param>
        /// <param name="pointPosition"> The point to evaluate. </param>
        ///
        /// <returns> Length. </returns>
        internal double GetHypotenuse2DFromPoint(Position2 referencePosition, Position2 pointPosition)
        {
            double lengthxy = 0.0D;
            try
            {
                double x1 = referencePosition.X;
                double y1 = referencePosition.Y;
                double x2 = pointPosition.X;
                double y2 = pointPosition.Y;

                lengthxy = Math.Sqrt(Math.Pow(x2 - x1, 2) + Math.Pow(y2 - y1, 2));
                return lengthxy;

            }
            catch (Exception ex)
            {
                throw ex;
            }
        }

        /// <summary> Gets the 2D hypotenuse between 3D threeVector3 points. </summary>
        ///
        /// <exception cref="Exception"> Thrown when an exception error condition occurs. </exception>
        ///
        /// <param name="referencePosition"> The reference point. </param>
        /// <param name="pointToEvaluate"> The point to evaluate. </param>
        ///
        /// <returns> Length. </returns>
        internal double GetHypotenuse2DFrom3DVectorlPoints(threeVector3 referencePosition, threeVector3 pointToEvaluate)
        {
            double lengthxy = 0.0D;
            try
            {
                double x1 = referencePosition.x;
                double y1 = referencePosition.y;
                double x2 = pointToEvaluate.x;
                double y2 = pointToEvaluate.y;

                lengthxy = Math.Sqrt(Math.Pow(x2 - x1, 2) + Math.Pow(y2 - y1, 2));
                return lengthxy;

            }
            catch (Exception ex)
            {
                throw ex;
            }
        }


        /// <summary> Minimum reductive. </summary>
        ///
        /// <param name="point"> The current edge or corner point being evaluated. </param>
        public static double D_Min_Reductive(Point point)
        {
            double H;
            double W;
            double d_min;

            H = point.Position.Z;
            W = point.Level.BoundingBox.MinimumWidth;

            // 𝑑_𝑚𝑖𝑛=(3.8𝐻_2^0.78 𝑊_2^0.28)/2
            d_min = Math.Pow(3.8 * H, 0.78) * Math.Pow(W, 0.28) / 2;

            return d_min;
        }

        /// <summary> Gets magic number. </summary>
        ///
        /// <param name="d_2D"> The 2D. </param>
        /// <param name="H_cp"> The cp. </param>
        /// <param name="W_cp"> The cp. </param>
        public static double GetMagicNumber(double d_2D, double H_cp, double W_cp)
        {
            double M;

            // 𝑀=1/(𝑑_2𝐷+1)∗〖𝐻_𝐶𝑃〗^0.8∗〖𝑊_𝐶𝑃〗^0.3
            M = 1 / (d_2D + 1) * Math.Pow(H_cp, 0.8) * Math.Pow(W_cp, 0.3);

            return M;
        }
    }
}