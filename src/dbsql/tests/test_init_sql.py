import os
import re
import pytest
import sqlfluff

current_dir = os.path.dirname(os.path.abspath(__file__))


class TestClassDBmodel:

    def test_init_sql(self):
        for full_path, dirs, filenames in os.walk(current_dir+"/../"):
            for filename in filenames:
                if re.match(r"^.+\.sql$", filename):
                    with open(current_dir+f"/../{filename}", "r") as f:
                        # result = sqlfluff.parse(f.read(), dialect="mysql")
                        # print(result)
                        pass