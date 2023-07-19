import pandas as pd


def get_distance_of_coordinate_between_two_time_stamps(coordinate1, coordinate2) -> float:
    """Calculate the distance between two points in space"""
    return coordinate2 - coordinate1


def get_table_of_deltas_between_time_stamps_in_all_kps(x_y_data: pd.DataFrame) -> pd.DataFrame:
    """Calculate the difference between the coordinates of the key points in two consecutive time stamps
    Args:
        x_y_data (pd.DataFrame): data frame of values for every key point (column) and time stamp (row)
    Vars:
        counter_of_all_zeros_in_a_row_for_all_kps (dict): dictionary of dictionaries that are counters of consecutive
                                                            zeros in a row for all key points
    Returns:
        deltas (df): data frame of deltas between each 2 consecutive time stamps (0-1, 1-2, 2-3, etc.)
                        Each row corresponds to the difference between two consecutive time stamps.
    Algorithm:
        If the value in the time stamp is 0, then the value in the delta is 0.
        If the value in the time stamp is not 0, then the value in the delta is the difference between the value in the
        time stamp and the value in the previous time stamp, that is not 0.

    """
    deltas = pd.DataFrame(columns=x_y_data.columns)
    counter_of_all_zeros_in_a_row_for_all_kps = dict()

    for kp in x_y_data.columns:
        counter_of_all_zeros_in_a_row_for_all_kps[kp] = dict()
        loc_of_last_timestamp_before_zero = 0
        counter_of_zeros_in_a_row = 0
        for time_stamp in range(len(x_y_data)-1):
            if x_y_data[kp][time_stamp] != 0 and x_y_data[kp][time_stamp+1] != 0:
                deltas[kp][time_stamp] = get_distance_of_coordinate_between_two_time_stamps(x_y_data[kp][time_stamp],
                                                                                            x_y_data[kp][time_stamp+1])
                continue
            if x_y_data[kp][time_stamp] == 0 and x_y_data[kp][time_stamp+1] != 0:
                loc_of_time_stamp = loc_of_last_timestamp_before_zero
                this_time_stamp_value = x_y_data[kp][loc_of_time_stamp]  # last value before zero values
                next_time_stamp_value = x_y_data[kp][time_stamp+1]
                deltas[kp][time_stamp] = get_distance_of_coordinate_between_two_time_stamps(this_time_stamp_value,
                                                                                            next_time_stamp_value)
                counter_of_all_zeros_in_a_row_for_all_kps[kp][time_stamp] = counter_of_zeros_in_a_row
                counter_of_zeros_in_a_row = 0
                continue
            if x_y_data[kp][time_stamp] == 0 and x_y_data[kp][time_stamp+1] == 0:
                counter_of_zeros_in_a_row += 1
                deltas[kp][time_stamp] = 0
                continue
            if x_y_data[kp][time_stamp] != 0 and x_y_data[kp][time_stamp+1] == 0:
                loc_of_last_timestamp_before_zero = time_stamp
                deltas[kp][time_stamp] = 0
                counter_of_zeros_in_a_row = 1
                continue
    return deltas