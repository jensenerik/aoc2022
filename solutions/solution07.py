from typing import Dict, List, NamedTuple

import solutions

example = """$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k"""


class FileModel(NamedTuple):
    file_name: str
    file_size: int
    full_path: List[str]


class FileSystemState(NamedTuple):
    current_path: List[str]
    files: List[FileModel]

    def return_to_root(self):
        self.current_path == []

    def back_out_directory(self):
        self.current_path.pop()

    def subdirectory(self, subdir_name: str):
        self.current_path.append(subdir_name)

    def add_file(self, file_name: str, file_size: int):
        self.files.append(FileModel(file_name, file_size, self.current_path.copy()))

    def parse_line(self, line: str):
        if line[0:4] == "$ cd":
            dir_arg = line[5:]
            if dir_arg == "/":
                self.return_to_root()
            elif dir_arg == "..":
                self.back_out_directory()
            else:
                self.subdirectory(dir_arg)
        elif line == "$ ls" or line[0:3] == "dir":
            pass
        else:
            file_data = line.split()
            self.add_file(file_data[1], int(file_data[0]))


def process_commands(commands: str) -> FileSystemState:
    file_system = FileSystemState([], [])
    for row in commands.split("\n"):
        file_system.parse_line(row)
    return file_system


def inclusive_sizes(file_system: FileSystemState) -> Dict[str, int]:
    directories: Dict[str, int] = {}
    for file in file_system.files:
        for i in range(len(file.full_path) + 1):
            partial_path = "/" + "/".join(file.full_path[0:i])
            prior_size = directories.get(partial_path, 0)
            directories[partial_path] = prior_size + file.file_size
    return directories


def sum_under_threshold(path_sizes: Dict[str, int], threshold: int) -> int:
    return sum([path_sizes[path] for path in path_sizes if path_sizes[path] <= threshold])


def smallest_under_threshold(path_sizes: Dict[str, int], total_disk: int, required_space: int) -> int:
    total_needed = required_space - total_disk + path_sizes["/"]
    return min([path_sizes[path] for path in path_sizes if path_sizes[path] >= total_needed])


assert sum_under_threshold(inclusive_sizes(process_commands(example)), 100000) == 95437
assert smallest_under_threshold(inclusive_sizes(process_commands(example)), 70000000, 30000000) == 24933642

directory_sizes = inclusive_sizes(process_commands(solutions.read_input("07")))
with open("outputs/output07.txt", "w") as file:
    file.write(str(sum_under_threshold(directory_sizes, 100000)))
    file.write("\n")
    file.write(str(smallest_under_threshold(directory_sizes, 70000000, 30000000)))
