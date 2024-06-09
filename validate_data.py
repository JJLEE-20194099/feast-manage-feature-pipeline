import pandas as pd
from feast import FeatureStore
from feast.dqm.profilers.ge_profiler import ge_profiler
from great_expectations.core.expectation_suite import ExpectationSuite
from great_expectations.dataset import PandasDataset

store = FeatureStore(repo_path="feature_repo/")

# Getting a saved dataset
dataset = store.get_saved_dataset(name="realestate_dataset_1")

DELTA = 0.1
@ge_profiler
def stats_profiler(ds: PandasDataset) -> ExpectationSuite:
    # DEFINING MINIMUM AND MAXIMUM
    # EXPECTED VALUES

    # Getting min and max values for used_area
    observed_min = ds["used_area"].min()
    observed_max = ds["used_area"].max()

    # Setting the expected min and max values
    ds.expect_column_values_to_be_between(
        column="used_area",
        mostly=0.99,
        min_value=observed_min,
        max_value=observed_max
    )

    # DEFINING EXPECTED AVERAGE

    # Getting the average of used_area
    observed_mean = ds["used_area"].mean()

    # Setting the expected range
    ds.expect_column_mean_to_be_between(
        column="used_area",
        min_value=observed_mean * (1 - DELTA),
        max_value=observed_mean * (1 + DELTA)
    )

    # Retrieving comparison results
    return ds.get_expectation_suite(discard_failed_expectations=False)

print(dataset.get_profile(profiler=stats_profiler))