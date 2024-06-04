// Copyright (c) 2022 Applied Software Technology, Inc.

namespace nVentErico.LPSD.Controllers.Cvm
{
    /// <summary> Values that represent the type of units used. </summary>
    public enum Units
    {
        /// <summary> Imperial units option. </summary>
        Imperial,
        /// <summary> Metric units option. </summary>
        Metric
    }
    /// <summary> Values that represent POI (point of interest) locations on the structure. </summary>
    public enum PoiLocation
    {
        /// <summary> The POI is not set option. </summary>
        NotSet,
        /// <summary> The POI is on the Corner of a structure's roof. </summary>
        None,
        /// <summary> The No POI Location. </summary>
        Corner,
        /// <summary> The POI is on the Edge of a structure's roof. </summary>
        Edge,
        /// <summary> The POI is on an Extended Edge of a structure's roof. </summary>
        ExtendedEdge,
        /// <summary> The POI is in the Middle of a structure's roof. </summary>
        Middle,
        /// <summary> The POI is on a Gable Ridge Corner of a structure's roof. </summary>
        GableRidgeCorner,
        /// <summary> The POI is on a Gable Ridge Edge of a structure's roof. </summary>
        GableRidgeEdge,
        /// <summary> The POI is on a Gable Sloped Edge of a structure's roof. </summary>
        GableSlope,
        /// <summary> The POI is on a Gable Eave Corner of a structure's roof. </summary>
        GableEaveCorner,
        /// <summary> The POI is on a Gable Eave Edge of a structure's roof. </summary>
        GableEaveEdge,
    }

    /// <summary> Values that represent the types of Air Terminals. </summary>
    public enum AirTerminalType
    {
        /// <summary> A series 3000 dynasphere terminal. </summary>
        Dynasphere,
        /// <summary> A passive air terminal. </summary>
        Passive,
    }

    /// <summary> Values that represent the geometric shape of a structure's level. </summary>
    public enum LevelShape
    {
        /// <summary> Shape is not set. </summary>
        NotSet,
        /// <summary> The geometric shape of a structure's level is a rectangle. </summary>
        Rectangle,
        /// <summary> The geometric shape of a structure's level is an oval. </summary>
        Oval,
        /// <summary> An enum constant representing the hybrid option.
        ///           This Level contains both oval and rectangular points </summary>
        //Hybrid,
        /// <summary> The geometric shape of a structure's level is a gable. </summary>
        Gable,
    }

    /// <summary> Values that represent the geometric shape of a gable roof. </summary>

    public enum GableShape
    {
        /// <summary> Shape is not set. </summary>
        NotSet,
        /// <summary> The geometric shape of a standard gable roof. </summary>
        Gable,
        /// <summary> The geometric shape of a shed roof. </summary>
        Shed,
        /// <summary> The geometric shape of a broken gable roof.</summary>
        Broken,
        /// <summary> The geometric shape of a gambrel roof. </summary>
        Gambrel,
    }

    /// <summary> Values that represent ki calculation types. </summary>
    public enum KiCalculationType
    {
        /// <summary> An enum constant representing the Ki calculation type. </summary>
        General,
        /// <summary> Calculations are multiplicative. </summary>
        Multiplicative,
        /// <summary> Calculations are reductive. </summary>
        Reductive,
    }
}