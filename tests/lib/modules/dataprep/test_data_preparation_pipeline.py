import pytest

SCOPE = "function"


@pytest.fixture(scope=SCOPE)
def fxt_lib_modules_dataprep(mocker):
    from lib.modules.data_prep.data_preparation_pipeline import run_data_prep

    mocker.patch(
        "lib.modules.data_prep.data_preparation_pipeline.run_data_retrieval",
        mocker.MagicMock(),
    )
    mocker.patch(
        "lib.modules.data_prep.data_preparation_pipeline.run_data_quality_pipeline",
        mocker.MagicMock(),
    )
    mocker.patch(
        "lib.modules.data_prep.data_preparation_pipeline.load_datasrc_config",
        mocker.MagicMock(),
    )
    mocker.patch(
        "lib.modules.data_prep.data_preparation_pipeline.run_move_file",
        mocker.MagicMock(),
    )
    mocker.patch(
        "lib.modules.data_prep.data_preparation_pipeline.run_data_preprocessing_pipeline",
        mocker.MagicMock(),
    )


def test_run_dataprep(fxt_lib_modules_dataprep):
    list_datasrc = ["datasrc1", "datasrc2"]
    from lib.modules.data_prep.data_preparation_pipeline import run_data_prep

    res = run_data_prep(list_datasrc)
    assert set(list(res.keys())).issubset(set(list_datasrc))
    assert len(list_datasrc) == len(res.keys())
