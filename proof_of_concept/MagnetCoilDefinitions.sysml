package MagnetCoilDefinitions {

    private import ISQ::*;
    private import SI::*;
    private import ScalarValues::*;

    part def MagnetCoil {
        doc /* A superconducting magnet coil for plasma confinement. */

        attribute majorRadius : ISQ::LengthValue;
        attribute minorRadius : ISQ::LengthValue;
        attribute peakField : ISQ::MagneticFluxDensityValue;
        attribute turns : ScalarValues::Natural;
        attribute currentPerTurn : ISQ::ElectricCurrentValue;
    }

    calc def StoredEnergy {
        doc /* Magnetic stored energy: E = 0.5 * L * I^2,
               approximated here as E ~ B^2 * Volume / (2 * mu0). */

        in peakField : ISQ::MagneticFluxDensityValue;
        in volume : ISQ::VolumeValue;

        attribute mu0 : Real = 1.2566e-6;

        return energy : Real =
            0.5 * peakField * peakField * volume / mu0;
    }

    calc def CoilVolume {
        doc /* Toroidal coil volume approximation: V = 2 * pi^2 * R * r^2 */

        in majorRadius : ISQ::LengthValue;
        in minorRadius : ISQ::LengthValue;

        return volume : ISQ::VolumeValue =
            2.0 * 3.14159 * 3.14159 * majorRadius * minorRadius * minorRadius;
    }
}
