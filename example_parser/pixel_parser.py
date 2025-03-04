from common.environment import PixelEnvironment
from common.experiment import Example, TestCase
from example_parser.parser import Parser

class PixelParser(Parser):

    def __init__(self, path: str = None, result_folder_path: str = None):
        super().__init__(
            domain_name="pixel",
            path=path or "examples/e3-pixels/data/",
            result_folder_path=result_folder_path or "results/e3-pixels/"
        )

    def _parse_file_lines(self, file_name: str, lines: 'list[str]') -> (list[Example], list[Example]):
        # get first line and remove unneeded characters.
        line = lines[0][4:-2]

        # splits into input and output
        entries = line.split("w(")[1:]
        
        example = Example(
            PixelParser._parse_entry(entries[0]),
            PixelParser._parse_entry(entries[1]),
        )

        return [example], [example]

    @staticmethod
    def _parse_entry(entry: str) -> PixelEnvironment:
        # parses first four entries about position of pointer and width and height.
        e = list(map(
            PixelParser._parse_value,
            entry[:-2].split(',')[:4]
        ))

        # retries the actual array and split by ','
        arr = entry.split("[")[1].split("]")[0].split(",")
        (width, height) = (e[2], e[3])
        pixels = tuple([bool(int(e)) for e in arr])

        return PixelEnvironment(
            x=e[0]-1, y=e[1]-1,
            width=width,
            height=height,
            pixels=pixels
        )

    @staticmethod
    def _parse_value(val: str) -> int:
        # casts to int if numeric, 0 otherwise.
        if val.isnumeric():
            return int(val)
        return 1

if __name__ == "__main__":
    res1 = PixelParser(path="../examples/e3-pixels/data/").parse()
    n = 10
    for res in res1.test_cases:
        n -= 1
        if n == 0:
            break

        print(res.file_name)
        print(res.training_examples[0].input_environment)
        print(res.training_examples[0].output_environment)
