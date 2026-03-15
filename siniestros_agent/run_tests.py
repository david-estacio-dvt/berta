"""Quick test runner."""
import sys, json
sys.path.insert(0, '.')
from simulation_test import *
passed = 0; failed = 0; errors = []
def run(cls, m):
    global passed, failed
    try: getattr(cls(), m)(); passed += 1
    except Exception as e: failed += 1; errors.append(f"  {cls.__name__}.{m}: {e}")

for m in ['test_valid_initial_codes','test_transition_100_to_200','test_transition_100_to_900','test_transition_100_to_500_invalid','test_transition_200_to_328','test_transition_500_to_600','test_transition_600_to_700','test_transition_999_terminal','test_all_codes_have_definitions','test_code_info']:
    run(TestCASStateMachine, m)
for m in ['test_find_by_matricula','test_find_by_dni','test_not_found','test_no_params']:
    run(TestVerifyInjuredPerson, m)
for m in ['test_policy_active','test_policy_expired','test_policy_not_found','test_policy_out_of_dates']:
    run(TestVerifyInsurance, m)
for m in ['test_accident_found','test_accident_by_matricula','test_accident_not_found']:
    run(TestVerifyAccident, m)
for m in ['test_new_expediente_initial_code','test_new_expediente_invalid_code','test_existing_expediente_valid','test_existing_expediente_invalid']:
    run(TestCASCodeSequence, m)
for m in ['test_hospital_adherido','test_hospital_no_encontrado','test_hospital_inactivo','test_hospital_convenio_diferente']:
    run(TestHospitalAdhesion, m)
for m in ['test_within_limits','test_exceeds_limits','test_empty_services']:
    run(TestTariffs, m)
for m in ['test_coherent_cervical_rear','test_incoherent','test_unknown_accident_type']:
    run(TestInjuryConsistency, m)
for m in ['test_valid_dates','test_assistance_before_accident','test_outside_convention']:
    run(TestDateValidation, m)
for m in ['test_expediente_found','test_expediente_not_found']:
    run(TestCaseHistory, m)
for m in ['test_generate_acceptance','test_generate_invalid_transition','test_generate_rehuse']:
    run(TestResponseGeneration, m)
for m in ['test_full_acceptance_flow','test_rehuse_flow_expired_policy','test_existing_expediente_flow']:
    run(TestCASFlowIntegration, m)
for m in ['test_list_test_files','test_read_real_pdf','test_expediente_with_real_docs']:
    run(TestRealCaseFiles, m)
print(f"TOTAL: {passed} passed, {failed} failed")
if errors:
    print("FAILURES:"); [print(e) for e in errors]
else:
    print("ALL TESTS PASSED!")
