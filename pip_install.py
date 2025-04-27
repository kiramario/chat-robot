import datetime, sys, subprocess
from pathlib import Path
from pyparsing import Word, nums, Literal, Combine

def write_requirement(installed: str):
    
    requirement_path = Path.cwd() / "requirements.txt"
    
    if not requirement_path.exists():
        with open(str(requirement_path), 'w', encoding="utf-8") as f:
            pass

    with open(str(requirement_path), "a+") as f:
        f.writelines(installed+"\n")

def parse_install_info(stdout_str: str, package_name: str):
    dash = Literal("-")
    version = Combine(Word(nums) + ("." + Word(nums)) * (1, 2))
    package_expr = Combine(Literal(package_name) + dash + version)
    res = package_expr.searchString(stdout_str)
    if len(res) == 0:
        return ""
    return res[0][0]

def run(package_name: str):
    cmd_install = [sys.executable, "-m", "pip", "install", package_name]
    p = subprocess.Popen(cmd_install,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)

    stdout, stderr = p.communicate()

    if isinstance(stdout, bytes):
        stdout = stdout.decode('utf-8')

    print(f"install info: {stdout}")

    installed = parse_install_info(stdout, package_name)

    if installed:
        package_name_end_index = installed.index(package_name) + len(package_name)
        to_write = installed[0 : package_name_end_index] + "==" + installed[package_name_end_index + 1:]

        write_requirement(to_write)
    else:
        print("nothing write")

str_out = """
Collecting pywebview
  Downloading pywebview-5.4-py3-none-any.whl.metadata (4.5 kB)
Collecting pythonnet (from pywebview)
  Downloading pythonnet-3.0.5-py3-none-any.whl.metadata (6.6 kB)
Collecting proxy_tools (from pywebview)
  Downloading proxy_tools-0.1.0.tar.gz (3.0 kB)
  Preparing metadata (setup.py): started
  Preparing metadata (setup.py): finished with status 'done'
Collecting bottle (from pywebview)
  Downloading bottle-0.13.3-py2.py3-none-any.whl.metadata (2.1 kB)
Requirement already satisfied: typing_extensions in c:\alluserapplication\anaconda3\envs\worldquant\lib\site-packages (from pywebview) (4.13.2)
Collecting clr_loader<0.3.0,>=0.2.7 (from pythonnet->pywebview)
  Downloading clr_loader-0.2.7.post0-py3-none-any.whl.metadata (1.5 kB)
Collecting cffi>=1.17 (from clr_loader<0.3.0,>=0.2.7->pythonnet->pywebview)
  Downloading cffi-1.17.1-cp311-cp311-win_amd64.whl.metadata (1.6 kB)
Collecting pycparser (from cffi>=1.17->clr_loader<0.3.0,>=0.2.7->pythonnet->pywebview)
  Using cached pycparser-2.22-py3-none-any.whl.metadata (943 bytes)
Downloading pywebview-5.4-py3-none-any.whl (475 kB)
Downloading bottle-0.13.3-py2.py3-none-any.whl (104 kB)
Downloading pythonnet-3.0.5-py3-none-any.whl (297 kB)
Downloading clr_loader-0.2.7.post0-py3-none-any.whl (50 kB)
Downloading cffi-1.17.1-cp311-cp311-win_amd64.whl (181 kB)
Using cached pycparser-2.22-py3-none-any.whl (117 kB)
Building wheels for collected packages: proxy_tools
  DEPRECATION: Building 'proxy_tools' using the legacy setup.py bdist_wheel mechanism, which will be removed in a future version. pip 25.3 will enforce this behaviour change. A possible replacement is to use the standardized build interface by setting the `--use-pep517` option, (possibly combined with `--no-build-isolation`), or adding a `pyproject.toml` file to the source tree of 'proxy_tools'. Discussion can be found at https://github.com/pypa/pip/issues/6334
  Building wheel for proxy_tools (setup.py): started
  Building wheel for proxy_tools (setup.py): finished with status 'done'
  Created wheel for proxy_tools: filename=proxy_tools-0.1.0-py3-none-any.whl size=2944 sha256=74e8538fe46d253fbbfc621006c83cc3d4f561084be97ee8f9ae028802ee5174
  
Successfully built proxy_tools
Installing collected packages: proxy_tools, bottle, pycparser, cffi, clr_loader, pythonnet, pywebview

Successfully installed bottle-0.13.3 cffi-1.17.1 clr_loader-0.2.7.post0 proxy_tools-0.1.0 pycparser-2.22 pythonnet-3.0.5 pywebview-5.4
"""

if __name__ == "__main__":
    package_name = "jieba" if len(sys.argv) == 1 else sys.argv[1]

    start = datetime.datetime.now()
    run(package_name)

    # print(parse_install_info(str_out, package_name))
    exec_time = (datetime.datetime.now() - start).total_seconds()
    print(f"run total spend: {exec_time:.3f}s\n")


