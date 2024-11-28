import mlreserve as cl

def test_basic_odp_cl(genins):
    assert abs(
        (cl.Chainladder().fit(genins).ultimate_ -
         cl.Chainladder().fit(cl.MLReserve().fit_transform(genins)).ultimate_) /
        genins.latest_diagonal).max()< 1e-2
