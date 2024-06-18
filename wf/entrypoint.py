from dataclasses import dataclass
from enum import Enum
import os
import subprocess
import requests
import shutil
from pathlib import Path
import typing
import typing_extensions

from latch.resources.workflow import workflow
from latch.resources.tasks import nextflow_runtime_task, custom_task
from latch.types.file import LatchFile
from latch.types.directory import LatchDir, LatchOutputDir
from latch.ldata.path import LPath
from latch_cli.nextflow.workflow import get_flag
from latch_cli.nextflow.utils import _get_execution_name
from latch_cli.utils import urljoins
from latch.types import metadata
from flytekit.core.annotation import FlyteAnnotation

from latch_cli.services.register.utils import import_module_by_path

meta = Path("latch_metadata") / "__init__.py"
import_module_by_path(meta)
import latch_metadata

@custom_task(cpu=0.25, memory=0.5, storage_gib=1)
def initialize() -> str:
    token = os.environ.get("FLYTE_INTERNAL_EXECUTION_ID")
    if token is None:
        raise RuntimeError("failed to get execution token")

    headers = {"Authorization": f"Latch-Execution-Token {token}"}

    print("Provisioning shared storage volume... ", end="")
    resp = requests.post(
        "http://nf-dispatcher-service.flyte.svc.cluster.local/provision-storage",
        headers=headers,
        json={
            "storage_gib": 100,
        }
    )
    resp.raise_for_status()
    print("Done.")

    return resp.json()["name"]






@nextflow_runtime_task(cpu=4, memory=8, storage_gib=100)
def nextflow_runtime(pvc_name: str, input: str, outdir: typing.Optional[typing_extensions.Annotated[LatchDir, FlyteAnnotation({'output': True})]], email: typing.Optional[str], reference: str, save_trimmed_fail: typing.Optional[bool], subsampling_off: typing.Optional[bool], genome_size: typing.Optional[str], remove_recombination: typing.Optional[bool], rapidnj: typing.Optional[bool], fasttree: typing.Optional[bool], iqtree: typing.Optional[bool], raxmlng: typing.Optional[bool], enable_conda: typing.Optional[bool], show_hidden_params: typing.Optional[bool], trim: typing.Optional[bool], adapter_file: typing.Optional[str], subsampling_depth_cutoff: typing.Optional[int], non_GATC_threshold: typing.Optional[float], validate_params: typing.Optional[bool]) -> None:
    try:
        shared_dir = Path("/nf-workdir")



        ignore_list = [
            "latch",
            ".latch",
            "nextflow",
            ".nextflow",
            "work",
            "results",
            "miniconda",
            "anaconda3",
            "mambaforge",
        ]

        shutil.copytree(
            Path("/root"),
            shared_dir,
            ignore=lambda src, names: ignore_list,
            ignore_dangling_symlinks=True,
            dirs_exist_ok=True,
        )

        cmd = [
            "/root/nextflow",
            "run",
            str(shared_dir / "main.nf"),
            "-work-dir",
            str(shared_dir),
            "-profile",
            "docker",
            "-c",
            "latch.config",
                *get_flag('input', input),
                *get_flag('outdir', outdir),
                *get_flag('email', email),
                *get_flag('reference', reference),
                *get_flag('trim', trim),
                *get_flag('save_trimmed_fail', save_trimmed_fail),
                *get_flag('adapter_file', adapter_file),
                *get_flag('subsampling_off', subsampling_off),
                *get_flag('subsampling_depth_cutoff', subsampling_depth_cutoff),
                *get_flag('genome_size', genome_size),
                *get_flag('remove_recombination', remove_recombination),
                *get_flag('non_GATC_threshold', non_GATC_threshold),
                *get_flag('rapidnj', rapidnj),
                *get_flag('fasttree', fasttree),
                *get_flag('iqtree', iqtree),
                *get_flag('raxmlng', raxmlng),
                *get_flag('enable_conda', enable_conda),
                *get_flag('validate_params', validate_params),
                *get_flag('show_hidden_params', show_hidden_params)
        ]

        print("Launching Nextflow Runtime")
        print(' '.join(cmd))
        print(flush=True)

        env = {
            **os.environ,
            "NXF_HOME": "/root/.nextflow",
            "NXF_OPTS": "-Xms2048M -Xmx8G -XX:ActiveProcessorCount=4",
            "K8S_STORAGE_CLAIM_NAME": pvc_name,
            "NXF_DISABLE_CHECK_LATEST": "true",
        }
        subprocess.run(
            cmd,
            env=env,
            check=True,
            cwd=str(shared_dir),
        )
    finally:
        print()

        nextflow_log = shared_dir / ".nextflow.log"
        if nextflow_log.exists():
            name = _get_execution_name()
            if name is None:
                print("Skipping logs upload, failed to get execution name")
            else:
                remote = LPath(urljoins("latch:///your_log_dir/nf_nf_core_bactmap", name, "nextflow.log"))
                print(f"Uploading .nextflow.log to {remote.path}")
                remote.upload_from(nextflow_log)



@workflow(metadata._nextflow_metadata)
def nf_nf_core_bactmap(input: str, outdir: typing.Optional[typing_extensions.Annotated[LatchDir, FlyteAnnotation({'output': True})]], email: typing.Optional[str], reference: str, save_trimmed_fail: typing.Optional[bool], subsampling_off: typing.Optional[bool], genome_size: typing.Optional[str], remove_recombination: typing.Optional[bool], rapidnj: typing.Optional[bool], fasttree: typing.Optional[bool], iqtree: typing.Optional[bool], raxmlng: typing.Optional[bool], enable_conda: typing.Optional[bool], show_hidden_params: typing.Optional[bool], trim: typing.Optional[bool] = True, adapter_file: typing.Optional[str] = '${baseDir}/assets/adapters.fas', subsampling_depth_cutoff: typing.Optional[int] = 100, non_GATC_threshold: typing.Optional[float] = 0.5, validate_params: typing.Optional[bool] = True) -> None:
    """
    nf-core/bactmap

    Sample Description
    """

    pvc_name: str = initialize()
    nextflow_runtime(pvc_name=pvc_name, input=input, outdir=outdir, email=email, reference=reference, trim=trim, save_trimmed_fail=save_trimmed_fail, adapter_file=adapter_file, subsampling_off=subsampling_off, subsampling_depth_cutoff=subsampling_depth_cutoff, genome_size=genome_size, remove_recombination=remove_recombination, non_GATC_threshold=non_GATC_threshold, rapidnj=rapidnj, fasttree=fasttree, iqtree=iqtree, raxmlng=raxmlng, enable_conda=enable_conda, validate_params=validate_params, show_hidden_params=show_hidden_params)

