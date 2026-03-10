package TokamakMagnetUsage {

    private import MagnetCoilDefinitions::*;
    private import ISQ::*;
    private import SI::*;

    part tokamakTFCoil : MagnetCoil {
        doc /* Toroidal field coil sized to ITER-class parameters. */

        attribute redefines majorRadius = 6.2 [m];
        attribute redefines minorRadius = 2.0 [m];
        attribute redefines peakField = 11.8 [T];
        attribute redefines turns = 134;
        attribute redefines currentPerTurn = 68000.0 [A];
    }

    calc tfCoilVolume : CoilVolume {
        in majorRadius = tokamakTFCoil.majorRadius;
        in minorRadius = tokamakTFCoil.minorRadius;
    }

    calc tfStoredEnergy : StoredEnergy {
        in peakField = tokamakTFCoil.peakField;
        in volume = tfCoilVolume.volume;
    }
}
