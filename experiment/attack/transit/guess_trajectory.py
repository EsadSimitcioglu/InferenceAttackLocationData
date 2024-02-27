import csv

from experiment.attack.metrics import normalized_distance_error, prediction_accuracy, experiment_metrics


def ratio_of_guess(true_value_list, guess_value_list):
    prob_sum = 0
    index_counter = 0

    for guess_value, true_value in zip(guess_value_list, true_value_list):
        if guess_value == true_value:
            prob_sum += 1
        index_counter += 1

    return prob_sum / index_counter


def perturb(protocol, user_trajectory_list):
    reports = list()
    for user_index, user_trajectory in enumerate(user_trajectory_list):
        if protocol.is_hash_used:
            report = ([protocol.client(user_value, user_index + 1) for user_value in user_trajectory])
        else:
            report = ([protocol.client(user_value) for user_value in user_trajectory])

        if protocol.is_bit_vector:
            report = [protocol.convert_binary_report_to_decimal(report_string) for report_string in report]
        reports.append(report)
    return reports


def guess_plain_user_trajectory(protocol, hmm_model, user_trajectory_list, test_type='PA', dataset_name=None):
    report_list = perturb(protocol, user_trajectory_list)
    hmm_model.create_plain_protocol_model(protocol)
    guess_list = [hmm_model.guess_user_values(protocol, report) for report in report_list]
    return experiment_metrics(test_type, user_trajectory_list, guess_list, dataset_name)

def guess_plain_user_trajectory_olh(protocol, hmm_model, user_trajectory_list, test_type='PA', dataset_name=None):
    report_list = perturb(protocol, user_trajectory_list)
    guess_list = list()
    for user_index, report in enumerate(report_list):
        hmm_model.create_plain_protocol_model(protocol, user_index + 1)
        guess_list.append(hmm_model.guess_user_values(protocol, report))
    return experiment_metrics(test_type, user_trajectory_list, guess_list, dataset_name)


def guess_fk_user_trajectory(protocol, hmm_model, user_trajectory_list, test_type='PA', dataset_name=None):
    report_list = perturb(protocol, user_trajectory_list)
    hmm_model.create_advance_protocol_model(protocol, user_trajectory_list)
    guess_list = [hmm_model.guess_user_values(report) for report in report_list]
    return experiment_metrics(test_type, user_trajectory_list, guess_list, dataset_name)


def guess_fk_user_trajectory_olh(protocol, hmm_model, user_trajectory_list, test_type='PA', dataset_name=None):
    report_list = perturb(protocol, user_trajectory_list)
    guess_list = list()
    for user_index, report in enumerate(report_list):
        hmm_model.create_advance_protocol_model(protocol, user_trajectory_list, user_index + 1)
        guess_list.append(hmm_model.guess_user_values(report))
    return experiment_metrics(test_type, user_trajectory_list, guess_list, dataset_name)


def guess_advance_user_trajectory(protocol, hmm_model, user_trajectory_list, test_count, test_type='PA', dataset_name=None):
    hmm_model.create_plain_protocol_model(protocol)

    for _ in range(test_count):
        report_list = perturb(protocol, user_trajectory_list)
        guess_list = [hmm_model.guess_user_values(report) for report in report_list]
        hmm_model.create_advance_protocol_model(protocol, guess_list)

    report_list = perturb(protocol, user_trajectory_list)
    guess_list = [hmm_model.guess_user_values(report) for report in report_list]
    return experiment_metrics(test_type, user_trajectory_list, guess_list, dataset_name)


def guess_advance_user_trajectory_olh(protocol, hmm_model, user_trajectory_list, test_count, test_type='PA',
                                      dataset_name=None):
    report_list = perturb(protocol, user_trajectory_list)
    guess_list = list()

    for user_index, report in enumerate(report_list):
        hmm_model.create_plain_protocol_model(protocol, user_index + 1)

        for _ in range(test_count):
            test_report_list = perturb(protocol, [user_trajectory_list[user_index]])
            guess_list = [hmm_model.guess_user_values(report) for report in test_report_list]
            hmm_model.create_advance_protocol_model(protocol, guess_list, user_index + 1)

        guess_list.append(hmm_model.guess_user_values(report))
    return experiment_metrics(test_type, user_trajectory_list, guess_list, dataset_name)
