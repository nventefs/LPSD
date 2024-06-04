// Copyright (c) 2022 Applied Software Technology, Inc.

using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Text.RegularExpressions;
using System.Xml.Serialization;

using nVentErico.LPSD.Controllers.Cvm;
using Point = nVentErico.LPSD.Controllers.Cvm.Point;
using Newtonsoft.Json.Linq;

namespace nVentErico.LPSD.BaseClasses.Cvm
{
    /// <summary> Base class for the nVent Test process engines. </summary>
    public class CvmBase
    {
        /// <summary> Gets or sets the JSON cvm data to process. </summary>
        public JObject JsonCvmDataToProcess { get; set; }

        /// <summary> Gets or sets the JSON data string for test case 1. </summary>
        public string JsonTestCase_1 { get; set; }

        /// <summary> Gets or sets the JSON data string for test case 2. </summary>
        public string JsonTestCase_2 { get; set; }

        /// <summary> Gets or sets the error traces. </summary>
        public static List<string> ErrorTraces { get; set; } = new List<string>();

        /// <summary> Gets or sets the CVM engine. </summary>
        public CvmEngine CvmEngine { get; set; }

        /// <summary> Gets or sets the full pathname of the assembly file. </summary>
        public static string AssemblyPath { get; set; }

        /// <summary> Gets or sets the current product version. </summary>
        public static string CurrentApplicationVersion { get; set; } = string.Empty;

        /// <summary> Gets or sets the current job identifier. </summary>
        public static string CurrentTestMethod { get; set; } = string.Empty;

        /// <summary> Gets or sets the vault property values. </summary>
        public static Dictionary<string, string> VaultPropertyValues { get; set; } = new Dictionary<string, string>();

        /// <summary> Gets or sets the site. </summary>
        public Site Site { get; set; } = new Site();

        /// <summary> Gets or sets the building. </summary>
        public Building Building { get; set; } = new Building();

        /// <summary> Gets or sets the level. </summary>
        public Level Level { get; set; } = new Level();

        /// <summary> Gets or sets the poi point. </summary>
        public Point PoiPoint { get; set; } = new Point();

        /// <summary> Gets or sets the bounding box. </summary>
        public BoundingBox BoundingBox { get; set; } = new BoundingBox();

        /// <summary> Gets or sets the terminal. </summary>
        public Terminal Terminal { get; set; }

        /// <summary> Gets or sets a dictionary of input points. </summary>
        public Dictionary<int, Point> InputPointDictionary { get; set; } = new Dictionary<int, Point>();

        /// <summary> Gets or sets the excel multiplicative results. </summary>
        public Dictionary<string, double> ExcelMultiplicativeResults { get; set; } = new Dictionary<string, double>();

        /// <summary> Gets or sets the excel reductive results. </summary>
        public Dictionary<string, Dictionary<int, object>> ExcelReductiveResults { get; set; } = new Dictionary<string, Dictionary<int, object>>();

        /// <summary> Gets or sets a dictionary of results. </summary>
        public Dictionary<string, double> ResultDictionary { get; set; } = new Dictionary<string, double>();

        /// <summary> Default constructor. </summary>
        public CvmBase()
        {
        }

        /// <summary> Gets multiplicative formulas. </summary>
        ///
        /// <param name="site"> The site. </param>
        /// <param name="building"> The building. </param>
        /// <param name="baseLevelOfBuilding"> The base level of building. </param>
        /// <param name="poiPoint"> The poi point. </param>
        /// <param name="terminal"> The terminal. </param>
        /// <param name="userCookie"> The user cookie. </param>
        public List<string> GetMultiplicativeFormulas(Site site, Building building, Level baseLevelOfBuilding, Point poiPoint, Terminal terminal, dynamic userCookie)
        {
            return ExceptionHandledOperation<List<string>>(() =>
            {
                var formulaLetters = new List<string>();

                var formula1 = GetMultiplicativeFormula_1(terminal, userCookie);
                formulaLetters.AddRange(formula1);

                var formula2 = GetMultiplicativeFormula_2(terminal, userCookie);
                formulaLetters.AddRange(formula2);

                var formula3 = GetMultiplicativeFormula_3(terminal, poiPoint, userCookie);
                formulaLetters.AddRange(formula3);

                var formula4 = GetMultiplicativeFormula_4(poiPoint, terminal, userCookie);
                formulaLetters.AddRange(formula4);

                var formula5 = GetMultiplicativeFormula_5(building, poiPoint, terminal, userCookie);
                formulaLetters.AddRange(formula5);

                return formulaLetters;

            }, "GetMultiplicativeFormulas");
        }

        /// <summary> Gets multiplicative formula 1. </summary>
        ///
        /// <param name="terminal"> The terminal. </param>
        /// <param name="userCookie"> The user cookie. </param>
        public List<string> GetMultiplicativeFormula_1(Terminal terminal, dynamic userCookie)
        {
            return ExceptionHandledOperation<List<string>>(() =>
            {
                var formula1Letters = new List<string>();

                //////////////   Equation 1   //////////////

                if (terminal != null && terminal.Method == "Collection Volume")
                {
                    formula1Letters.Add("H");
                }
                if (terminal != null && terminal.Method != "Collection Volume")
                {
                    formula1Letters.Add("I");
                }

                return formula1Letters;

            }, "GetMultiplicativeFormula_1");
        }

        /// <summary> Gets multiplicative formula 2. </summary>
        ///
        /// <param name="terminal"> The terminal. </param>
        /// <param name="userCookie"> The user cookie. </param>
        public List<string> GetMultiplicativeFormula_2(Terminal terminal, dynamic userCookie)
        {
            return ExceptionHandledOperation<List<string>>(() =>
            {
                var formula2Letters = new List<string>();

                //////////////   Equation 2  //////////////                

                if (terminal != null)
                {
                    switch (terminal.PoiPoint.Level.LevelShape)
                    {
                        case LevelShape.NotSet:
                            break;
                        case LevelShape.Rectangle:
                            switch (terminal.PoiPoint.LocationOnStucture)
                            {
                                case PoiLocation.Corner:
                                    formula2Letters.Add("T");
                                    break;
                                case PoiLocation.Edge:
                                    formula2Letters.Add("U");
                                    break;
                                case PoiLocation.Middle:
                                    formula2Letters.Add("V");
                                    break;
                                default:
                                    break;
                            }
                            break;
                        case LevelShape.Oval:
                            switch (terminal.PoiPoint.LocationOnStucture)
                            {
                                case PoiLocation.Edge:
                                    formula2Letters.Add("W");
                                    break;
                                case PoiLocation.Middle:
                                    formula2Letters.Add("X");
                                    break;
                                default:
                                    break;
                            }
                            break;
                        case LevelShape.Gable:
                            switch (terminal.PoiPoint.LocationOnStucture)
                            {
                                case PoiLocation.GableEaveCorner:
                                    formula2Letters.Add("Y");
                                    break;
                                case PoiLocation.GableEaveEdge:
                                    formula2Letters.Add("Z");
                                    break;
                                case PoiLocation.GableRidgeCorner:
                                    formula2Letters.Add("Y");
                                    break;
                                case PoiLocation.GableRidgeEdge:
                                    formula2Letters.Add("Z");
                                    break;
                                default:
                                    break;
                            }
                            break;
                        //case LevelShape.Hybrid:
                        //    if (terminal.PoiPoint.IsEdgeRectangular || terminal.PoiPoint.IsCorner || terminal.PoiPoint.IsFaceHorizontal)
                        //    {
                        //        switch (terminal.PoiPoint.LocationOnStucture)
                        //        {
                        //            case PoiLocation.Corner:
                        //                formula2Letters.Add("T");
                        //                break;
                        //            case PoiLocation.Edge:
                        //                formula2Letters.Add("U");
                        //                break;
                        //            case PoiLocation.Middle:
                        //                formula2Letters.Add("V");
                        //                break;
                        //            default:
                        //                break;
                        //        }
                        //        break;

                        //    }
                        //    if (terminal.PoiPoint.IsEdgeOval || terminal.PoiPoint.IsFaceHorizontal)
                        //    {
                        //        switch (terminal.PoiPoint.LocationOnStucture )
                        //        {
                        //            case PoiLocation.Edge:
                        //                formula2Letters.Add("W");
                        //                break;
                        //            case PoiLocation.Middle:
                        //                formula2Letters.Add("X");
                        //                break;
                        //            default:
                        //                break;
                        //        }
                        //    }
                        //    break;

                        default:
                            break;
                    }
                }
                return formula2Letters;

            }, "GetMultiplicativeFormula_2");
        }

        /// <summary> Gets multiplicative formula 3. </summary>
        ///
        /// <param name="terminal"> The terminal. </param>
        /// <param name="poiPoint"> The poi point. </param>
        /// <param name="userCookie"> The user cookie. </param>
        public List<string> GetMultiplicativeFormula_3(Terminal terminal, Point poiPoint, dynamic userCookie)
        {
            return ExceptionHandledOperation<List<string>>(() =>
            {
                var formula3Letters = new List<string>();

                //////////////   Equation  3   //////////////                

                if (terminal != null && !terminal.Level.LevelNumber.Equals(0D))
                {
                    if (!poiPoint.IsExtendedCornerOrEdge)
                    {
                        switch (poiPoint.Level.LevelShape)
                        {
                            case LevelShape.Rectangle:
                                switch (poiPoint.LocationOnStucture)
                                {
                                    case PoiLocation.Corner:
                                        formula3Letters.Add("J5");
                                        break;
                                    case PoiLocation.Edge:
                                        formula3Letters.Add("K5");
                                        break;
                                    case PoiLocation.Middle:
                                        formula3Letters.Add("L5");
                                        break;
                                    default:
                                        break;
                                }
                                break;
                            case LevelShape.Oval:
                                switch (poiPoint.LocationOnStucture)
                                {
                                    case PoiLocation.Edge:
                                        formula3Letters.Add("M5");
                                        break;
                                    case PoiLocation.Middle:
                                        formula3Letters.Add("N5");
                                        break;
                                    default:
                                        break;
                                }
                                break;
                            case LevelShape.Gable:
                                switch (poiPoint.LocationOnStucture)
                                {
                                    case PoiLocation.GableEaveCorner:
                                        formula3Letters.Add("O");
                                        break;
                                    case PoiLocation.GableEaveEdge:
                                        formula3Letters.Add("P");
                                        break;
                                    case PoiLocation.GableRidgeCorner:
                                        formula3Letters.Add("O");
                                        break;
                                    case PoiLocation.GableRidgeEdge:
                                        formula3Letters.Add("P");
                                        break;
                                    default:
                                        break;
                                }
                                break;
                            //case LevelShape.Hybrid:
                            //    if (terminal.PoiPoint.IsEdgeRectangular || terminal.PoiPoint.IsCorner || terminal.PoiPoint.IsFaceHorizontal)
                            //    {
                            //        switch (terminal.PoiPoint.LocationOnStucture)
                            //        {
                            //            case PoiLocation.Corner:
                            //                formula3Letters.Add("J5");
                            //                break;
                            //            case PoiLocation.Edge:
                            //                formula3Letters.Add("K5");
                            //                break;
                            //            case PoiLocation.Middle:
                            //                formula3Letters.Add("L5");
                            //                break;
                            //            default:
                            //                break;
                            //        }
                            //        break;
                            //    }
                            //    if (terminal.PoiPoint.IsEdgeOval || terminal.PoiPoint.IsFaceHorizontal)
                            //    {
                            //        switch (terminal.PoiPoint.LocationOnStucture)
                            //        {
                            //            case PoiLocation.Edge:
                            //                formula3Letters.Add("M5");
                            //                break;
                            //            case PoiLocation.Middle:
                            //                formula3Letters.Add("N5");
                            //                break;
                            //            default:
                            //                break;
                            //        }
                            //    }
                            //    break;

                            default:
                                break;
                        }
                    }
                }
                if (terminal == null && !poiPoint.Level.LevelNumber.Equals(0D)) // 2024.03.06 Added !level0 check
                {
                    if (!poiPoint.IsExtendedCornerOrEdge)
                    {
                        switch (poiPoint.Level.LevelShape)
                        {
                            case LevelShape.Rectangle:

                                switch (poiPoint.LocationOnStucture)
                                {
                                    case PoiLocation.Corner:
                                        formula3Letters.Add("A");
                                        break;
                                    case PoiLocation.Edge:
                                        formula3Letters.Add("B");
                                        break;
                                    case PoiLocation.Middle:
                                        formula3Letters.Add("C");
                                        break;
                                    default:
                                        break;
                                }
                                break;

                            case LevelShape.Oval:
                                switch (poiPoint.LocationOnStucture)
                                {
                                    case PoiLocation.Edge:
                                        formula3Letters.Add("D");
                                        break;
                                    case PoiLocation.Middle:
                                        formula3Letters.Add("E");
                                        break;
                                    default:
                                        break;
                                }
                                break;

                            case LevelShape.Gable:
                                switch (poiPoint.LocationOnStucture)
                                {
                                    case PoiLocation.GableEaveCorner:
                                        formula3Letters.Add("F");
                                        break;
                                    case PoiLocation.GableEaveEdge:
                                        formula3Letters.Add("G");
                                        break;
                                    case PoiLocation.GableRidgeCorner:
                                        formula3Letters.Add("F");
                                        break;
                                    case PoiLocation.GableRidgeEdge:
                                        formula3Letters.Add("G");
                                        break;
                                    case PoiLocation.GableSlope:
                                        formula3Letters.Add("G");
                                        break;
                                    default:
                                        break;
                                }
                                break;

                            //case LevelShape.Hybrid:
                            //    if (terminal.PoiPoint.IsEdgeRectangular || terminal.PoiPoint.IsCorner || terminal.PoiPoint.IsFaceHorizontal)
                            //    {
                            //        switch (poiPoint.LocationOnStucture)
                            //        {
                            //            case PoiLocation.Corner:
                            //                formula3Letters.Add("A");
                            //                break;
                            //            case PoiLocation.Edge:
                            //                formula3Letters.Add("B");
                            //                break;
                            //            case PoiLocation.Middle:
                            //                formula3Letters.Add("C");
                            //                break;
                            //            default:
                            //                break;
                            //        }
                            //        break;
                            //    }
                            //    if (terminal.PoiPoint.IsEdgeOval || terminal.PoiPoint.IsFaceHorizontal)
                            //    {
                            //        switch (poiPoint.LocationOnStucture)
                            //        {
                            //            case PoiLocation.Edge:
                            //                formula3Letters.Add("D");
                            //                break;
                            //            case PoiLocation.Middle:
                            //                formula3Letters.Add("E");
                            //                break;
                            //            default:
                            //                break;
                            //        }
                            //    }
                            //    break;

                            default:
                                break;
                        }
                    }
                }

                return formula3Letters;

            }, "GetMultiplicativeFormula_3");
        }

        /// <summary> Gets multiplicative formula 4. </summary>
        ///
        /// <param name="poiPoint"> The poi point. </param>
        /// <param name="terminal"> (Optional) The terminal. </param>
        /// <param name="userCookie"> (Optional) The user cookie. </param>
        public List<string> GetMultiplicativeFormula_4(Point poiPoint, Terminal terminal = null, dynamic userCookie = null)
        {
            return ExceptionHandledOperation<List<string>>(() =>
            {
                var formula4Letters = new List<string>();

                //////////////   Equation  4   //////////////                
                if (terminal == null && !poiPoint.Level.LevelNumber.Equals(0D)) // 2024.03.06 Added !level0 check
                {
                    if (!poiPoint.IsExtendedCornerOrEdge)
                    {
                        switch (poiPoint.Level.LevelShape)
                        {
                            case LevelShape.Rectangle:

                                switch (poiPoint.LocationOnStucture)
                                {
                                    case PoiLocation.Corner:
                                        formula4Letters.Add("Q");
                                        break;
                                    case PoiLocation.Edge:
                                        formula4Letters.Add("R");
                                        break;
                                    case PoiLocation.Middle:
                                        formula4Letters.Add("S");
                                        break;
                                    default:
                                        break;
                                }
                                break;

                            case LevelShape.Oval:
                                switch (poiPoint.LocationOnStucture)
                                {
                                    case PoiLocation.Edge:
                                        formula4Letters.Add("R");
                                        break;
                                    case PoiLocation.Middle:
                                        formula4Letters.Add("S");
                                        break;
                                    default:
                                        break;
                                }
                                break;

                            case LevelShape.Gable:
                                switch (poiPoint.LocationOnStucture)
                                {
                                    case PoiLocation.GableEaveCorner:
                                        formula4Letters.Add("Q");
                                        break;
                                    case PoiLocation.GableEaveEdge:
                                        formula4Letters.Add("R");
                                        break;
                                    case PoiLocation.GableRidgeCorner:
                                        formula4Letters.Add("Q");
                                        break;
                                    case PoiLocation.GableRidgeEdge:
                                        formula4Letters.Add("R");
                                        break;
                                    case PoiLocation.GableSlope:
                                        formula4Letters.Add("R");
                                        break;
                                    default:
                                        break;
                                }
                                break;

                            //case LevelShape.Hybrid:
                            //    if (terminal.PoiPoint.IsEdgeRectangular || terminal.PoiPoint.IsCorner || terminal.PoiPoint.IsFaceHorizontal)
                            //    {
                            //        switch (terminal.PoiPoint.LocationOnStucture)
                            //        {
                            //            case PoiLocation.Corner:
                            //                formula4Letters.Add("Q");
                            //                break;
                            //            case PoiLocation.Edge:
                            //                formula4Letters.Add("R");
                            //                break;
                            //            case PoiLocation.Middle:
                            //                formula4Letters.Add("S");
                            //                break;
                            //            default:
                            //                break;
                            //        }
                            //        break;
                            //    }
                            //    if (poiPoint.IsEdgeOval)
                            //    {
                            //        switch (poiPoint.LocationOnStucture)
                            //        {
                            //            case PoiLocation.Edge:
                            //                formula4Letters.Add("R");

                            //                break;
                            //            case PoiLocation.Middle:
                            //                formula4Letters.Add("S");

                            //                break;
                            //            default:
                            //                break;
                            //        }
                            //    }
                            //    break;

                            default:
                                break;
                        }
                    }
                }
                if (terminal != null && !terminal.Level.LevelNumber.Equals(0D))
                {
                    if (!terminal.PoiPoint.IsExtendedCornerOrEdge)
                    {
                        formula4Letters.Letters.Add("S");
                        /* 
                        The documentation for Equation 4 in LPSD 3.0 shows that the interpretations are difficult to manage
                        and that typically the FIR will be pressed between 1.8 and 0.9.  For conservative decision choices
                        we are pression Formula S for all terminals which typically result in an FIR of 0.9 or a reduction in
                        the Ki by 10% resulting in a slightly lower collection volume.

                        To make changes to this part of the code please review EFM multiplicativity notes pg 32

                        switch (terminal.Level.LevelShape)
                        {
                            case LevelShape.Rectangle:
                                switch (terminal.PoiPoint.LocationOnStucture)
                                {
                                    case PoiLocation.Corner:
                                        formula4Letters.Add("Q");
                                        break;
                                    case PoiLocation.Edge:
                                        formula4Letters.Add("R");
                                        break;
                                    case PoiLocation.Middle:
                                        formula4Letters.Add("S");
                                        break;
                                    default:
                                        break;
                                }
                                break;
                            case LevelShape.Oval:
                                switch (terminal.PoiPoint.LocationOnStucture)
                                {
                                    case PoiLocation.Edge:
                                        formula4Letters.Add("R");
                                        break;
                                    case PoiLocation.Middle:
                                        formula4Letters.Add("S");
                                        break;
                                    default:
                                        break;
                                }
                                break; 
                            //case LevelShape.Hybrid:
                            //    {
                            //        if (poiPoint.IsEdgeRectangular || poiPoint.IsCorner)
                            //        {
                            //            switch (terminal.PoiPoint.LocationOnStucture)
                            //            {
                            //                case PoiLocation.Corner:
                            //                    formula4Letters.Add("Q");
                            //                    break;
                            //                case PoiLocation.Edge:
                            //                    formula4Letters.Add("R");
                            //                    break;
                            //                case PoiLocation.Middle:
                            //                    formula4Letters.Add("S");
                            //                    break;
                            //                default:
                            //                    break;
                            //            }
                            //            break;
                            //        }
                            //        if (poiPoint.IsEdgeOval)
                            //        {
                            //            switch (poiPoint.LocationOnStucture)
                            //            {
                            //                case PoiLocation.Edge:
                            //                    formula4Letters.Add("R");
                            //                    break;
                            //                case PoiLocation.Middle:
                            //                    formula4Letters.Add("S");
                            //                    break;
                            //                default:
                            //                    break;
                            //            }
                            //            break;
                            //        }
                            //    }
                            //    break;
                            
                            default:
                                break;
                        }
                    }
                    // Point is always over the middle of the lower level
                    if (!terminal.PoiPoint.IsExtendedCornerOrEdge)
                    {
                        switch (terminal.Level.LevelShape)
                        {
                            case LevelShape.Rectangle:
                                formula4Letters.Add("S");
                                break;

                            case LevelShape.Oval:
                                formula4Letters.Add("S");
                                break;

                            case LevelShape.Gable:
                                formula4Letters.Add("S");
                                break;

                                //case LevelShape.Hybrid:
                                //    formula4Letters.Add("S");
                                //    break;


                        }
                    }
                    */
                    }
                }
                return formula4Letters;

            }, "GetMultiplicativeFormula_4");
        }

        /// <summary> Gets multiplicative formula 5. </summary>
        ///
        /// <param name="building"> The building. </param>
        /// <param name="poiPoint"> The poi point. </param>
        /// <param name="terminal"> (Optional) The terminal. </param>
        /// <param name="userCookie"> (Optional) The user cookie. </param>
        public List<string> GetMultiplicativeFormula_5(Building building, Point poiPoint, Terminal terminal = null, dynamic userCookie = null)
        {
            return ExceptionHandledOperation<List<string>>(() =>
            {
                var formula5Letters = new List<string>();

                //////////////   Equation  5   //////////////  
                if (terminal == null)
                {
                    if (poiPoint.IsExtendedCornerOrEdge)
                    {
                        switch (poiPoint.Level.LevelShape)
                        {
                            case LevelShape.Rectangle:

                                switch (poiPoint.LocationOnStucture)
                                {
                                    case PoiLocation.Corner:
                                        formula5Letters.Add("A");
                                        break;
                                    case PoiLocation.Edge:
                                        formula5Letters.Add("B");
                                        break;
                                    case PoiLocation.Middle:
                                        formula5Letters.Add("C");
                                        break;
                                    default:
                                        break;
                                }
                                break;

                            case LevelShape.Oval:
                                switch (poiPoint.LocationOnStucture)
                                {
                                    case PoiLocation.Edge:
                                        formula5Letters.Add("D");
                                        break;
                                    case PoiLocation.Middle:
                                        formula5Letters.Add("E");
                                        break;
                                    default:
                                        break;
                                }
                                break;

                            case LevelShape.Gable:
                                switch (poiPoint.LocationOnStucture)
                                {
                                    case PoiLocation.GableEaveCorner:
                                        formula5Letters.Add("F");
                                        break;
                                    case PoiLocation.GableEaveEdge:
                                        formula5Letters.Add("G");
                                        break;
                                    case PoiLocation.GableRidgeCorner:
                                        formula5Letters.Add("F");
                                        break;
                                    case PoiLocation.GableRidgeEdge:
                                        formula5Letters.Add("G");
                                        break;
                                    case PoiLocation.GableSlope:
                                        formula5Letters.Add("G");
                                        break;
                                    default:
                                        break;
                                }
                                break;
                            //case LevelShape.Hybrid:
                            //    {
                            //        if (poiPoint.IsEdgeRectangular || poiPoint.IsCorner)
                            //        {
                            //            switch (terminal.PoiPoint.LocationOnStucture)
                            //            {
                            //                case PoiLocation.Corner:
                            //                    formula5Letters.Add("A");
                            //                    break;
                            //                case PoiLocation.Edge:
                            //                    formula5Letters.Add("B");
                            //                    break;
                            //                case PoiLocation.Middle:
                            //                    formula5Letters.Add("C");
                            //                    break;
                            //                default:
                            //                    break;
                            //            }
                            //            break;
                            //        }
                            //        if (poiPoint.IsEdgeOval)
                            //        {
                            //            switch (poiPoint.LocationOnStucture)
                            //            {
                            //                case PoiLocation.Edge:
                            //                    formula5Letters.Add("D");
                            //                    break;
                            //                case PoiLocation.Middle:
                            //                    formula5Letters.Add("E");
                            //                    break;

                            //                default:
                            //                    break;
                            //            }
                            //            break;
                            //        }
                            //    }
                            //    break;
                            default:
                                break;
                        }
                    }
                    // If poi is not on base level and not on extended, then the POI is always above a middle point
                    if (!poiPoint.IsExtendedCornerOrEdge)
                    {
                        if (poiPoint.Level.LevelNumber > building.BaseLevel.LevelNumber)
                        {
                            switch (poiPoint.Level.LevelShape)
                            {
                                case LevelShape.Rectangle:
                                    formula5Letters.Add("L");
                                    break;

                                case LevelShape.Oval:
                                    formula5Letters.Add("N");
                                    break;

                                case LevelShape.Gable:
                                    formula5Letters.Add("N");
                                    break;

                                //case LevelShape.Hybrid:
                                //    if (poiPoint.IsEdgeRectangular || poiPoint.IsCorner)
                                //    {
                                //        formula5Letters.Add("L");
                                //    }
                                //    if (poiPoint.IsEdgeOval)
                                //    {
                                //        formula5Letters.Add("N");
                                //    }
                                //    break;

                                default:
                                    break;
                            }
                        }
                        if (poiPoint.Level.LevelNumber == building.BaseLevel.LevelNumber)
                        {
                            switch (poiPoint.Level.LevelShape)
                            {
                                case LevelShape.Rectangle:
                                    switch (poiPoint.LocationOnStucture)
                                    {
                                        case PoiLocation.Corner:
                                            formula5Letters.Add("A");
                                            break;
                                        case PoiLocation.Edge:
                                            formula5Letters.Add("B");
                                            break;
                                        case PoiLocation.Middle:
                                            formula5Letters.Add("C");
                                            break;
                                        default:
                                            break;
                                    }
                                    break;

                                case LevelShape.Oval:
                                    switch (poiPoint.LocationOnStucture)
                                    {
                                        case PoiLocation.Edge:
                                            formula5Letters.Add("D");
                                            break;
                                        case PoiLocation.Middle:
                                            formula5Letters.Add("E");
                                            break;
                                        default:
                                            break;
                                    }
                                    break;

                                //case LevelShape.Hybrid:
                                //    if (poiPoint.IsEdgeRectangular || poiPoint.IsCorner)
                                //    {
                                //        switch (terminal.PoiPoint.LocationOnStucture)
                                //        {
                                //            case PoiLocation.Corner:
                                //                formula5Letters.Add("J");
                                //                break;
                                //            case PoiLocation.Edge:
                                //                formula5Letters.Add("K");
                                //                break;
                                //            case PoiLocation.Middle:
                                //                formula5Letters.Add("L");
                                //                break;
                                //            default:
                                //                break;
                                //        }
                                //        break;
                                //    }
                                //    if (poiPoint.IsEdgeOval)
                                //    {
                                //        switch (poiPoint.LocationOnStucture)
                                //        {
                                //            case PoiLocation.Edge:
                                //                formula5Letters.Add("M");
                                //                break;
                                //            case PoiLocation.Middle:
                                //                formula5Letters.Add("N");
                                //                break;
                                //            default:
                                //                break;
                                //        }
                                //        break;
                                //    }
                                //    break;
                                default:
                                    break;
                            }
                        }
                    }
                }
                if (terminal != null)
                {
                    if (terminal.PoiPoint.IsExtendedCornerOrEdge | poiPoint.Level.LevelNumber.Equals(0D))
                    {
                        switch (terminal.Level.LevelShape)
                        {
                            case LevelShape.Rectangle:
                                switch (terminal.PoiPoint.LocationOnStucture)
                                {
                                    case PoiLocation.Corner:
                                        formula5Letters.Add("J");
                                        break;
                                    case PoiLocation.Edge:
                                        formula5Letters.Add("K");
                                        break;
                                    case PoiLocation.Middle:
                                        formula5Letters.Add("L");
                                        break;
                                    default:
                                        break;
                                }
                                break;

                            case LevelShape.Oval:
                                switch (terminal.PoiPoint.LocationOnStucture)
                                {
                                    case PoiLocation.Edge:
                                        formula5Letters.Add("M");
                                        break;
                                    case PoiLocation.Middle:
                                        formula5Letters.Add("N");
                                        break;
                                    default:
                                        break;
                                }
                                break;
                            case LevelShape.Gable:
                                switch (poiPoint.LocationOnStucture)
                                {
                                    case PoiLocation.GableEaveCorner:
                                        formula5Letters.Add("O");
                                        break;
                                    case PoiLocation.GableEaveEdge:
                                        formula5Letters.Add("P");
                                        break;
                                    case PoiLocation.GableRidgeCorner:
                                        formula5Letters.Add("O");
                                        break;
                                    case PoiLocation.GableRidgeEdge:
                                        formula5Letters.Add("P");
                                        break;
                                    default:
                                        break;
                                }
                                break;

                                //case LevelShape.Hybrid:
                                //    if (poiPoint.IsEdgeRectangular || poiPoint.IsCorner)
                                //    {
                                //        switch (terminal.PoiPoint.LocationOnStucture)
                                //        {
                                //            case PoiLocation.Corner:
                                //                formula5Letters.Add("J");
                                //                break;
                                //            case PoiLocation.Edge:
                                //                formula5Letters.Add("K");
                                //                break;
                                //            case PoiLocation.Middle:
                                //                formula5Letters.Add("L");
                                //                break;

                                //            default:
                                //                break;
                                //        }
                                //        break;
                                //    }
                                //    if (poiPoint.IsEdgeOval)
                                //    {
                                //        switch (poiPoint.LocationOnStucture)
                                //        {
                                //            case PoiLocation.Edge:
                                //                formula5Letters.Add("M");
                                //                break;
                                //            case PoiLocation.Middle:
                                //                formula5Letters.Add("N");
                                //                break;

                                //            default:
                                //                break;
                                //        }
                                //        break;
                                //    }
                                //    break;
                        }
                    }
                    if (!terminal.PoiPoint.IsExtendedCornerOrEdge)
                    {
                        switch (terminal.Level.LevelShape)
                        {
                            case LevelShape.Rectangle:
                                formula5Letters.Add("L");
                                break;

                            case LevelShape.Oval:
                                formula5Letters.Add("M");
                                break;

                            case LevelShape.Gable:
                                formula5Letters.Add("N");
                                break;

                            //case LevelShape.Hybrid:
                            //    if (poiPoint.IsEdgeRectangular || poiPoint.IsCorner)
                            //    {
                            //        formula5Letters.Add("L");
                            //        break;
                            //    }
                            //    if (poiPoint.IsEdgeOval)
                            //    {
                            //        formula5Letters.Add("N");
                            //        break;
                            //    }
                            //    break;
                            default:
                                break;
                        }
                    }
                }

                return formula5Letters;

            }, "GetMultiplicativeFormula_5");
        }

        /// <summary> Method determines if two doubles are roughly equivalent. </summary>
        ///
        /// <param name="d1"> first double value. </param>
        /// <param name="d2"> second double value. </param>
        /// <param name="epsilon"> (Optional) the tolerance factor. </param>
        ///
        /// <returns> Returns true if equivalent, otherwise false. </returns>
        private bool ApproximatelyEqualDoubles(double d1, double d2, double epsilon = 0.01255D)
        {
            return Math.Abs(d1 - d2) < epsilon;
        }

        #region Helper Methods


        /// <summary> Gets assembly path for this Vault extension. </summary>
        public string GetAssemblyPath()
        {
            return ExceptionHandledOperation<string>(() =>
            {
                string prefix = "file:///";
                string codebase = System.Reflection.Assembly.GetExecutingAssembly().CodeBase;
                if (codebase.StartsWith(prefix))
                {
                    codebase = codebase.Substring(prefix.Length);
                }

                return Path.GetDirectoryName(codebase);

            }, "GetAssemblyPath");
        }

        /// <summary> set the charge initially based on the protection level. </summary>
        ///
        /// <param name="terminal"> The terminal. </param>
        /// <param name="protectionLevelStr"> The protection level of the system 3000 terminal. </param>
        /// <param name="siteElevation"> The elevation of terminal. </param>
        /// <param name="terminalHeightAboveLevel"> The height the terminal is above the level's elevation. </param>
        public Terminal SetKeyParametersForTerminal(Terminal terminal, string protectionLevelStr, double siteElevation, double terminalHeightAboveLevel)
        {
            try
            {
                terminal.HeightAboveStructure = terminalHeightAboveLevel;
                terminal.H_Site = siteElevation;

                int level = 0;

                switch (protectionLevelStr)
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
            }

            return null;
        }

        /// <summary> Gets the hypotenuse from 3D point to points. </summary>
        ///
        /// <param name="referencePosition"> The terminal location. </param>
        /// <param name="pointPosition"> The point to evaluate. </param>
        ///
        /// <returns> Length. </returns>
        internal double GetHypotenuse3DFromPoint(Position2 referencePosition, Position2 pointPosition)
        {
            double lengthxyz = 0.0D;
            return ExceptionHandledOperation<double>(() =>
            {
                double x1 = referencePosition.X;
                double y1 = referencePosition.Y;
                double z1 = referencePosition.Z;
                double x2 = pointPosition.X;
                double y2 = pointPosition.Y;
                double z2 = pointPosition.Z;

                lengthxyz = Math.Sqrt(Math.Pow(x2 - x1, 2) + Math.Pow(y2 - y1, 2) + Math.Pow(z2 - z1, 2));
                return lengthxyz;

            }, "GetHypotenuse3DFromPoint");
        }

        /// <summary> Gets the hypotenuse from 2D point to points. </summary>
        ///
        /// <param name="referencePosition"> The terminal location. </param>
        /// <param name="pointPosition"> The point to evaluate. </param>
        ///
        /// <returns> Length. </returns>
        internal double GetHypotenuse2DFromPoint(Position2 referencePosition, Position2 pointPosition)
        {
            double lengthxy = 0.0D;
            return ExceptionHandledOperation<double>(() =>
            {
                double x1 = referencePosition.X;
                double y1 = referencePosition.Y;
                double x2 = pointPosition.X;
                double y2 = pointPosition.Y;

                lengthxy = Math.Sqrt(Math.Pow(x2 - x1, 2) + Math.Pow(y2 - y1, 2));
                return lengthxy;

            }, "GetHypotenuse2DFromPoint");
        }


        /// <summary>
        /// Writes the error information to a file whose path is set in the App.config file. This is utilized to create a
        /// file with exception and stack trace messages for error tracing.
        /// </summary>
        ///
        /// <param name="messages"> The messages. </param>
        /// <param name="name"> Brief name describing the information being output. This serves as the base of the file name
        ///                     as the ".txt" extension will be added automatically by this method to produce the destination
        ///                     file name. </param>
        /// <param name="currentTestMethod"> (Optional) The name of the current test method </param>
        //public static void WriteErrorTraceLogToFile(IList<string> messages, string name, string currentTestMethod = "")
        //{
        //    if (messages == null || !messages.Any())
        //    {
        //        return;
        //    }

        //    var sb = new StringBuilder();

        //    foreach (var message in messages)
        //    {
        //        sb.AppendLine(message);
        //    }

        //    sb.AppendLine(" nVent Unit Test Version: " + CurrentApplicationVersion);
        //    sb.AppendLine(" Executing nVent Unit Tests");

        //    var errorMessages = sb.ToString();

        //    try
        //    {
        //        var path = XmlSettings.ErrorLogOutputPath;

        //        if (path == string.Empty)
        //        {
        //            return;
        //        }

        //        // If the directory already exists, this method does not create a new directory, 
        //        // but it returns a DirectoryInfo object for the existing directory.
        //        System.IO.DirectoryInfo di = System.IO.Directory.CreateDirectory(path);

        //        if (di != null)
        //        {
        //            // Sterilize the exception name for placement within the error log file full path:
        //            name = name.Contains(":") ? name.Replace(':', ' ') : name;
        //            name = RemoveSpecialCharacters(name);

        //            var fileName = string.Format(@"{0}_Log_{1}.txt", name, DateTime.Now.ToString("yyyy-MM-dd_HHmm"));
        //            var outputFile = System.IO.Path.Combine(path, fileName);

        //            System.IO.File.WriteAllText(outputFile, string.Join(Environment.NewLine, errorMessages));
        //        }
        //    }
        //    catch (Exception ex)
        //    {
        //        ErrorTraces.Add(ex.Message);
        //        ErrorTraces.Add(ex.StackTrace);
        //        WriteErrorTraceLogToFile(ErrorTraces, "WriteErrorTraceLogToFile", CurrentTestMethod);
        //    }
        //}

        /// <summary> Removes the special characters contained within the string passed in. </summary>
        ///
        /// <param name="str"> The string passed into the method. </param>
        public static string RemoveSpecialCharacters(string str)
        {
            if (str != null)
            {
                return Regex.Replace(str, @"[^a-zA-Z0-9_.'!@#$%^&*()--=+/\s]+", "", RegexOptions.Compiled);
            }
            else { return null; }
        }

        #endregion Helper Methods

        #region Exception Wrappers

        /// <summary> Exception Handling Wrapper. </summary>
        ///
        /// <exception cref="Exception"> Thrown when an exception error condition occurs. </exception>
        ///
        /// <typeparam name="T"> . </typeparam>
        /// <param name="codeToExecute"> Func of T Delegate. </param>
        /// <param name="methodName"> Name of the calling method. </param>
        ///
        /// <returns> Type T. </returns>
        protected T ExceptionHandledOperation<T>(Func<T> codeToExecute, string methodName)
        {
            try
            {
                return codeToExecute.Invoke();
            }
            catch (Exception ex)
            {
                return default;
            }
        }

        /// <summary> Exception Handling Wrapper. </summary>
        ///
        /// <exception cref="Exception"> Thrown when an exception error condition occurs. </exception>
        ///
        /// <param name="codeToExecute"> Action Delegate. </param>
        /// <param name="methodName"> Name of the calling method. </param>
        protected void ExceptionHandledOperation(System.Action codeToExecute, string methodName)
        {
            try
            {
                codeToExecute.Invoke();
            }
            catch (Exception ex)
            {
            }
        }

        #endregion
    }
}
