import reframe as rfm
import reframe.utility.sanity as sn


@rfm.simple_test
class BuildCloverleafeTest(rfm.RegressionTest):
    descr = ('Build the Cloverleaf mini-app')
    valid_systems = ['archer2:compute']
    valid_prog_environs = ['PrgEnv-cray','PrgEnv-gnu','PrgEnv-aocc']
    #self.sourcesdir = None
    sourcesdir = 'https://github.com/UK-MAC/CloverLeaf_ref.git'
    executable = './clover_leaf'
    build_system = 'Make'
    num_tasks=8
    num_tasks_per_node=8
    num_cpus_per_task=16
    tags = {'production', 'craype'}

    @run_before('compile')
    def setflags(self):
        if self.current_environ.name.startswith('PrgEnv-gnu'):
            self.build_system.options = ['MPI_COMPILER=ftn C_MPI_COMPILER=cc C_OPTIONS="-O3 -fopenmp" OPTIONS="-O3 -fopenmp -fallow-argument-mismatch"']
        elif self.current_environ.name.startswith('PrgEnv-cray'):
            self.build_system.options = ['MPI_COMPILER=ftn C_MPI_COMPILER=cc C_OPTIONS="-O3 -fopenmp" OPTIONS="-O3 -homp"']
        elif self.current_environ.name.startswith('PrgEnv-aocc'):
            self.build_system.options = ['MPI_COMPILER=ftn C_MPI_COMPILER=cc C_OPTIONS="-O3 -fopenmp" OPTIONS="-O3 -fopenmp"']

    @sanity_function
    def assert_clover(self):
        return sn.assert_found(r'PASSED', self.stdout)

