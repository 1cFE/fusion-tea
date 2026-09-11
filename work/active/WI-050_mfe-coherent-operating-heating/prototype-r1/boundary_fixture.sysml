package boundary_fixture {
 private import ScalarValues::*;
 private import mfe_heating_chain::*;
 constraint def Upper { doc /* Fixture sustainment ceiling. */ in attribute demand : Real; in attribute capacity : Real; demand <= capacity }
 constraint def Lower { doc /* Fixture burn hold. */ in attribute demand : Real; demand >= 0.0 }
 part test {
  attribute demand : Real = 12.0;
  attribute installed : Real = 100.0;
  attribute source_eta : Real = 0.5;
  attribute couple_eta : Real = 0.75;
  calc heat : 'Heating Power Chain' { in p_wallplug = installed; in eta_source = source_eta; in eta_couple = couple_eta; }
  calc operating_heat : 'Operating Heating Power' { in p_required_in = demand; in eta_source_in = source_eta; in eta_couple_in = couple_eta; }
  assert constraint upper : Upper { in demand = operating_heat.p_coupled; in capacity = heat.p_coupled; }
  assert constraint lower : Lower { in demand = operating_heat.p_coupled; }
  assert constraint source_positive : 'Heating Efficiency Positive' { in efficiency = source_eta; }
  assert constraint source_upper : 'Heating Efficiency Upper' { in efficiency = source_eta; }
  assert constraint couple_positive : 'Heating Efficiency Positive' { in efficiency = couple_eta; }
  assert constraint couple_upper : 'Heating Efficiency Upper' { in efficiency = couple_eta; }
 }
 part def Legacy {
  attribute installed : Real default 0.0;
  attribute delivered_direct : Real default 50.0;
  attribute coupled_direct : Real default 30.0;
  attribute source_eta : Real default 0.5;
  attribute couple_eta : Real default 0.75;
  calc heat : 'Heating Power Chain' { in p_wallplug = installed; in p_delivered_direct = delivered_direct; in p_coupled_direct = coupled_direct; in eta_source = source_eta; in eta_couple = couple_eta; }
  attribute demand : Real default heat.p_coupled;
  calc operating_heat : 'Operating Heating Power' { in p_required_in = demand; in eta_source_in = source_eta; in eta_couple_in = couple_eta; }
 }
 part legacy : Legacy;
 part mixed : Legacy { :>> installed = 100.0; }
 part allzero : Legacy { :>> installed = 0.0; :>> delivered_direct = 0.0; :>> coupled_direct = 0.0; :>> source_eta = 1.0; :>> couple_eta = 1.0; }
}
