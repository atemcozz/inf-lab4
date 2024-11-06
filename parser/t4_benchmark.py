import time
import t0_dumb_parser as dumb_parser
import t1_lib_parser as lib_parser
import t2_regex_parser as regex_parser
import t3_fgrammar_parser as fgrammar_parser

with open("../resources/schedule.yml", "r", encoding="UTF-8") as fin:
    content = fin.read()

iterations = 100
print(f"{iterations} iterations:")


# Dumb parser
start_time = time.perf_counter()
for x in range(iterations):
    parsed = dumb_parser.yaml_to_json(content)
end_time = time.perf_counter()
print(f"Dumb parser: took {end_time - start_time}s")

# Lib parser
start_time = time.perf_counter()
for x in range(iterations):
    parsed = lib_parser.yaml_to_json(content)
end_time = time.perf_counter()
print(f"Lib parser: took {end_time - start_time}s")

# Regex parser
start_time = time.perf_counter()
for x in range(iterations):
    parsed = regex_parser.yaml_to_json(content)
end_time = time.perf_counter()
print(f"Regex parser: took {end_time - start_time}s")

# Formal grammar parser
start_time = time.perf_counter()
for x in range(iterations):
    parsed = fgrammar_parser.obj_to_json(fgrammar_parser.from_yaml(content))
end_time = time.perf_counter()
print(f"Formal grammar parser: took {end_time - start_time}s")