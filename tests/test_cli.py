# SPDX-License-Identifier: MIT

import unittest
from argparse import Namespace
from typing import List, Optional

import odxtools.cli.decode as decode
import odxtools.cli.find as find
import odxtools.cli.list as list_tool

import_failed = False

try:
    import odxtools.cli.browse as browse
except ImportError:
    import_failed = True


class UtilFunctions:

    @staticmethod
    def run_list_tool(path_to_pdx_file: str = "./examples/somersault.pdx",
                      ecu_variants: Optional[List[str]] = None,
                      print_neg_responses: bool = False,
                      ecu_services: Optional[List[str]] = None,
                      print_params: bool = False,
                      print_dops: bool = False,
                      print_all: bool = False,
                      plumbing_output: bool = False) -> None:
        list_args = Namespace(
            pdx_file=path_to_pdx_file,
            variants=ecu_variants,
            global_negative_responses=print_neg_responses,
            services=ecu_services,
            params=print_params,
            dops=print_dops,
            all=print_all,
            plumbing_output=plumbing_output)

        list_tool.run(list_args)

    @staticmethod
    def run_decode_tool(
        data: str,
        decode_data: bool = False,
        path_to_pdx_file: str = "./examples/somersault.pdx",
        ecu_variants: Optional[List[str]] = None,
    ) -> None:
        decode_args = Namespace(
            pdx_file=path_to_pdx_file, variants=ecu_variants, data=data, decode=decode_data)

        decode.run(decode_args)

    @staticmethod
    def run_find_tool(service_names: List[str],
                      path_to_pdx_file: str = "./examples/somersault.pdx",
                      ecu_variants: Optional[List[str]] = None,
                      allow_unknown_bit_lengths: bool = False,
                      no_details: bool = False,
                      plumbing_output: bool = False) -> None:
        find_args = Namespace(
            pdx_file=path_to_pdx_file,
            variants=ecu_variants,
            service_names=service_names,
            relaxed_output=allow_unknown_bit_lengths,
            no_details=no_details,
            plumbing_output=plumbing_output)

        find.run(find_args)


class TestCommandLineTools(unittest.TestCase):

    def test_list_tool(self) -> None:

        UtilFunctions.run_list_tool()
        UtilFunctions.run_list_tool(ecu_variants=["somersault"])
        UtilFunctions.run_list_tool(print_neg_responses=True)
        UtilFunctions.run_list_tool(print_params=True)
        UtilFunctions.run_list_tool(print_dops=True)
        UtilFunctions.run_list_tool(print_all=True)
        UtilFunctions.run_list_tool(plumbing_output=True)
        UtilFunctions.run_list_tool(ecu_services=["session_start"])

    def test_decode_tool(self) -> None:

        UtilFunctions.run_decode_tool(data="3E00")
        UtilFunctions.run_decode_tool(data="3e00")
        UtilFunctions.run_decode_tool(data="3E 00", decode_data=True)
        UtilFunctions.run_decode_tool(data="3E 00", ecu_variants=["somersault_lazy"])
        UtilFunctions.run_decode_tool(data="3E 00")

    def test_find_tool(self) -> None:
        UtilFunctions.run_find_tool(service_names=["headstand"])
        UtilFunctions.run_find_tool(service_names=["headstand"], allow_unknown_bit_lengths=True)
        UtilFunctions.run_find_tool(
            service_names=["headstand"], allow_unknown_bit_lengths=True, no_details=True)

    @unittest.skipIf(import_failed, "import of PyInquirer failed")
    def test_browse_tool(self) -> None:
        browse_args = Namespace(pdx_file="./examples/somersault.pdx")
        browse.run(browse_args)


if __name__ == "__main__":
    unittest.main()
