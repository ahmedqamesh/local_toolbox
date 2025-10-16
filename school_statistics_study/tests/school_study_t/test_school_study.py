from unittest import TestCase
from main_lib import school_study
import pandas as pd
import numpy as np
from unittest.mock import patch


class TestCore(TestCase):
    def setUp(self):
        self.app = school_study

    def test_read_excel_sheet_mocked(self):
        with patch('main_lib.school_study.pd.read_excel') as mock_read_excel, \
             patch('main_lib.school_study.pd.ExcelFile') as mock_excelfile:
            # Prepare mock DataFrames
            n = 100
            df_exam_mock = pd.DataFrame({
                'A': np.arange(0, n),
                'B': np.arange(0, n)
                })
            df_grade7_mock = pd.DataFrame({
                'Grade_7': np.random.randint(0, 100, size=n),
                'Grade_8': np.random.randint(0, 100, size=n)
                })

            # Configure the mock to return DataFrames
            mock_read_excel.side_effect = [df_exam_mock, df_grade7_mock]

            # Call the function
            df_exam, df_grade7 = self.app.read_excel_sheet("fake_file.xlsx")

            # Assertions
            self.assertTrue(mock_excelfile.called)
            self.assertEqual(mock_read_excel.call_count, 2)

            pd.testing.assert_frame_equal(df_exam, df_exam_mock)
            pd.testing.assert_frame_equal(df_grade7, df_grade7_mock)


if __name__ == "__main__":
    pass
