import numpy as np
import pytest
import mlreserve as cl

try:
    from rpy2.robjects.packages import importr
    from rpy2.robjects import r
    CL = importr("ChainLadder")
except:
    pass


def mack_r(data, alpha, est_sigma):
    return r(
        'mack<-MackChainLadder({},alpha={}, est.sigma="{}", tail=TRUE)'.format(
            data, alpha, est_sigma
        )
    )


def mack_p(data, average, est_sigma):
    return cl.TailCurve(curve="exponential").fit_transform(
        cl.Development(average=average, sigma_interpolation=est_sigma).fit_transform(
            cl.load_sample(data)
        )
    )


def mack_p_no_tail(data, average, est_sigma):
    return cl.Development(average=average, sigma_interpolation=est_sigma).fit_transform(
        cl.load_sample(data)
    )


data = ["RAA", "ABC", "GenIns", "MW2008", "MW2014"]
# M3IR5 in R fails silently on exponential tail. Python actually computes it.
averages = [("simple", 0), ("volume", 1), ("regression", 2)]
est_sigma = [("mack", "Mack"), ("log-linear", "log-linear")]


@pytest.mark.r
@pytest.mark.parametrize("data", data)
@pytest.mark.parametrize("averages", averages)
@pytest.mark.parametrize("est_sigma", est_sigma)
def test_mack_tail_ldf(data, averages, est_sigma, atol):
    p = mack_p(data, averages[0], est_sigma[0]).ldf_.set_backend("numpy", inplace=True)
    xp = p.get_array_module()
    r = xp.array(mack_r(data, averages[1], est_sigma[1]).rx("f"))
    p = xp.concatenate(
        (
            p.values[0, 0, :, :][:, :-2],
            xp.prod(p.values[0, 0, :, :][:, -2:], -1, keepdims=True),
        ),
        -1,
    )
    p = xp.unique(p, axis=-2)
    assert xp.allclose(r, p, atol=atol)


@pytest.mark.r
@pytest.mark.parametrize("data", data)
@pytest.mark.parametrize("averages", averages)
@pytest.mark.parametrize("est_sigma", est_sigma)
def test_mack_tail_sigma(data, averages, est_sigma, atol):
    p = mack_p(data, averages[0], est_sigma[0]).sigma_
    xp = p.get_array_module()
    r = xp.array(mack_r(data, averages[1], est_sigma[1]).rx("sigma"))
    p = xp.unique(p.values[0, 0, :, :], axis=-2)
    assert xp.allclose(r, p, atol=atol)


@pytest.mark.r
@pytest.mark.parametrize("data", data)
@pytest.mark.parametrize("averages", averages)
@pytest.mark.parametrize("est_sigma", est_sigma)
def test_mack_tail_std_err(data, averages, est_sigma, atol):
    p = mack_p(data, averages[0], est_sigma[0]).std_err_
    xp = p.get_array_module()
    r = xp.array(mack_r(data, averages[1], est_sigma[1]).rx("f.se"))
    p = xp.unique(p.values[0, 0, :, :], axis=-2)
    assert xp.allclose(r, p, atol=atol)


@pytest.mark.r
@pytest.mark.parametrize("data", data)
@pytest.mark.parametrize("averages", averages[0:1])
@pytest.mark.parametrize("est_sigma", est_sigma[0:1])
def test_tail_doesnt_mutate_std_err(data, averages, est_sigma):
    p = mack_p(data, averages[0], est_sigma[0]).std_err_
    xp = p.get_array_module()
    p_no_tail = mack_p_no_tail(data, averages[0], est_sigma[0]).std_err_.values
    xp.testing.assert_array_equal(p_no_tail, p.values[:, :, :, :-1])


@pytest.mark.r
@pytest.mark.parametrize("data", data)
@pytest.mark.parametrize("averages", averages[0:1])
@pytest.mark.parametrize("est_sigma", est_sigma[0:1])
def test_tail_doesnt_mutate_ldf_(data, averages, est_sigma):
    p = mack_p(data, averages[0], est_sigma[0]).ldf_
    xp = p.get_array_module()
    p_no_tail = mack_p_no_tail(data, averages[0], est_sigma[0]).ldf_.values
    xp.testing.assert_array_equal(
        p_no_tail, p.values[..., : len(cl.load_sample(data).ddims) - 1]
    )


@pytest.mark.r
@pytest.mark.parametrize("data", data)
@pytest.mark.parametrize("averages", averages[0:1])
@pytest.mark.parametrize("est_sigma", est_sigma[0:1])
def test_tail_doesnt_mutate_sigma_(data, averages, est_sigma):
    p = mack_p(data, averages[0], est_sigma[0]).sigma_
    xp = p.get_array_module()
    p_no_tail = mack_p_no_tail(data, averages[0], est_sigma[0]).sigma_.values
    xp.testing.assert_array_equal(p_no_tail, p.values[:, :, :, :-1])