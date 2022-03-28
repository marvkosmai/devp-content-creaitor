import pandas as pd
import pytest

import src.pipeline.Pipeline as Pipeline


class TestPipeline:
    def test_init(self):
        data = [1, 2, 3]
        P_test = Pipeline.Pipeline(data)
        P_data = P_test.data

        data_comp = P_test.data.equals(pd.DataFrame(data))
        processed_data_comp = P_test.processed_data.equals(pd.DataFrame(data))
        queue_comp = P_test.functions_queue == []
        assert data_comp and processed_data_comp and queue_comp

    def test_add_step(self):
        data = [1, 2, 3]
        P_test = Pipeline.Pipeline(data)
        P_test.add_step(print)
        P_queue = P_test.functions_queue
        assert P_queue == [print]

    def test_add_step_non_function(self):
        data = [1, 2, 3]
        P_test = Pipeline.Pipeline(data)
        with pytest.raises(TypeError):
            P_test.add_step(1)

    def test_run(self):
        data = [1, 2, 3]
        P_test = Pipeline.Pipeline(data)
        P_test.add_step(lambda x: x + 1)
        P_test.run()

        assert P_test.processed_data.equals(pd.DataFrame([2, 3, 4]))
