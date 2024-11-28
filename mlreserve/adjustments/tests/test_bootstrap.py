import mlreserve as cl
import numpy as np


def test_bs_sample(raa):
    tri = raa
    a = (
        cl.Development()
        .fit(cl.BootstrapODPSample(n_sims=40000).fit_transform(tri).mean())
        .ldf_
    )
    b = cl.Development().fit_transform(tri).ldf_
    assert tri.get_array_module().all(abs(((a - b) / b).values) < 0.005)

def test_bs_multiple_cols():
    assert cl.BootstrapODPSample().fit_transform(
        cl.load_sample('berqsherm').iloc[0]).shape == (1000, 4, 8, 8)
