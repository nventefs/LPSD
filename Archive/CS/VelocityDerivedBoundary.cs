// Copyright (c) 2022 Applied Software Technology, Inc.

using System.Collections.Generic;

namespace nVentErico.LPSD.Controllers.Cvm
{
    /// <summary> Data of a velocity derived boundary calculation. </summary>
    public class VelocityDerivedBoundary
    {
        /// <summary> Gets or sets the attractive radius. </summary>
        public double AttractiveRadius { get; set; }

        /// <summary> Gets or sets the total Z distance from the POI to the attractive radius. </summary>
        public double Z_r { get; set; }

        /// <summary> Gets or sets the H value for an air terminal tip above its POI Z value. </summary>
        public double AirTerminalTipAbovePoiLevel { get; set; }

        /// <summary> Gets or sets the striking distance. </summary>
        public double StrikingDistance { get; set; }

        /// <summary> Gets or sets the points for the Velocity Derived Boundary curve. </summary>
        public List<VelocityBoundaryPoint> VDB_Points { get; set; } = new List<VelocityBoundaryPoint>();

        /// <summary> Default constructor. </summary>
        public VelocityDerivedBoundary()
        {

        }

        /// <summary> Constructor. </summary>
        ///
        /// <param name="attractiveRadius"> The attractive radius. </param>
        /// <param name="z_r"> The r. </param>
        /// <param name="airTerminalTipAbovePoiLevel"> The air terminal tip above POI Z level. </param>
        /// <param name="strikingDistance"> The striking distance aka d_s derived from CVM down. </param>
        /// <param name="vdbPoints"> The vdb points. </param>
        public VelocityDerivedBoundary(double attractiveRadius, double z_r,
                                       double airTerminalTipAbovePoiLevel,
                                       double strikingDistance,
                                       List<VelocityBoundaryPoint> vdbPoints)
        {
            AttractiveRadius = attractiveRadius;
            Z_r = z_r;
            AirTerminalTipAbovePoiLevel = airTerminalTipAbovePoiLevel;
            StrikingDistance = strikingDistance;

            if (vdbPoints == null)
            {
                VDB_Points = new List<VelocityBoundaryPoint>();
            }
            else
            {
                VDB_Points = vdbPoints;
            }
        }
    }
}