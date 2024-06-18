
from dataclasses import dataclass
import typing
import typing_extensions

from flytekit.core.annotation import FlyteAnnotation

from latch.types.metadata import NextflowParameter
from latch.types.file import LatchFile
from latch.types.directory import LatchDir, LatchOutputDir

# Import these into your `__init__.py` file:
#
# from .parameters import generated_parameters

generated_parameters = {
    'input': NextflowParameter(
        type=str,
        default=None,
        section_title='Input/output options',
        description='Path to a sample sheet describing paths to input fastq files',
    ),
    'outdir': NextflowParameter(
        type=typing.Optional[typing_extensions.Annotated[LatchDir, FlyteAnnotation({'output': True})]],
        default=None,
        section_title=None,
        description='The output directory where the results will be saved.',
    ),
    'email': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Email address for completion summary.',
    ),
    'reference': NextflowParameter(
        type=str,
        default=None,
        section_title='Compulsory parameters',
        description='Path to a fasta file of the reference sequence',
    ),
    'trim': NextflowParameter(
        type=typing.Optional[bool],
        default=True,
        section_title='Optional pipeline steps',
        description='Trim reads',
    ),
    'save_trimmed_fail': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Saved failed read files after trimminng',
    ),
    'adapter_file': NextflowParameter(
        type=typing.Optional[str],
        default='${baseDir}/assets/adapters.fas',
        section_title=None,
        description='path to file containing adapters in fasta format',
    ),
    'subsampling_off': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Turn off subsampling',
    ),
    'subsampling_depth_cutoff': NextflowParameter(
        type=typing.Optional[int],
        default=100,
        section_title=None,
        description='Desired coverage depth when subsampling',
    ),
    'genome_size': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Specify genome size for subsampling rather than estimation using mash sketch',
    ),
    'remove_recombination': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Remove recombination using gubbins',
    ),
    'non_GATC_threshold': NextflowParameter(
        type=typing.Optional[float],
        default=0.5,
        section_title=None,
        description='Maximum non GATC bases (i.e - and N) to allow in pseudogenome sequences',
    ),
    'rapidnj': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Build a tree using the RapidNJ neighbour-joining algorithm',
    ),
    'fasttree': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Build a tree using the FastTree approximate ML algorithm',
    ),
    'iqtree': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Build a tree using the IQ-TREE ML algorithm',
    ),
    'raxmlng': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Build a tree using the RAxML-NG ML algorithm',
    ),
    'enable_conda': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title='Generic options',
        description='enable conda rather than use containers',
    ),
    'validate_params': NextflowParameter(
        type=typing.Optional[bool],
        default=True,
        section_title=None,
        description='Boolean whether to validate parameters against the schema at runtime',
    ),
    'show_hidden_params': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Show all params when using `--help`',
    ),
}

