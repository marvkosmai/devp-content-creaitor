import os.path

import pandas as pd
import pytest

import src.pipeline.Pipeline as Pipeline


class TestPipeline:
    def test_init(self):
        data = [1, 2, 3]
        p_test = Pipeline.Pipeline(pd.DataFrame(data))
        data_comp = p_test.data.equals(pd.DataFrame(data))
        processed_data_comp = p_test.processed_data.equals(pd.DataFrame(data))
        queue_comp = p_test.functions_queue == []
        assert data_comp and processed_data_comp and queue_comp

    def test_read_data_from_csv(self):
        test_file = 'csv_test_file.csv'
        data = [1, 2, 3]
        if os.path.isfile(test_file):
            raise FileExistsError('Test file exists. Aborting.')
        try:
            with open(test_file, mode='w') as file:
                file.write('1\n2\n3')
            p_test = Pipeline.Pipeline()
            p_test.read_data_from_csv(test_file, sep=',', header=None)
            equal = p_test.data.equals(pd.DataFrame(data))
            assert equal
        finally:
            os.remove(test_file)

    def test_batch_read_data_from_csv(self):
        test_file1 = 'csv_test_file1.csv'
        test_file2 = 'csv_test_file2.csv'
        data = [1, 2, 3, 4]
        if os.path.isfile(test_file1):
            raise FileExistsError('Test file 1 exists. Aborting.')
        if os.path.isfile(test_file2):
            raise FileExistsError('Test file 2 exists. Aborting.')
        try:
            with open(test_file1, mode='w') as file:
                file.write('1\n2')
            with open(test_file2, mode='w') as file:
                file.write('3\n4')
            csv_list = [test_file1, test_file2]
            p_test = Pipeline.Pipeline()
            p_test.batch_read_data_from_csv(csv_list, sep=',', header=None)
            equal = p_test.data.equals(pd.DataFrame(data))
            assert equal
        finally:
            os.remove(test_file1)
            os.remove(test_file2)

    def test_add_step(self):
        data = [1, 2, 3]
        p_test = Pipeline.Pipeline(pd.DataFrame(data))
        p_test.add_step(print)
        p_queue = p_test.functions_queue
        assert p_queue == [print]

    def test_add_step_non_function(self):
        data = [1, 2, 3]
        p_test = Pipeline.Pipeline(pd.DataFrame(data))
        with pytest.raises(TypeError):
            p_test.add_step(1)

    def test_remove_last_step(self):
        data = [1, 2, 3]
        p_test = Pipeline.Pipeline(pd.DataFrame(data))
        p_test.add_step(print)
        p_test.remove_last_step()
        assert p_test.functions_queue == []

    def test_run(self):
        data = [1, 2, 3]
        p_test = Pipeline.Pipeline(pd.DataFrame(data))
        p_test.add_step(lambda x: x + 1)
        p_test.run()

        assert p_test.processed_data.equals(pd.DataFrame([2, 3, 4]))
