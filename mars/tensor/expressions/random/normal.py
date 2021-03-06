#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 1999-2018 Alibaba Group Holding Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import numpy as np

from .... import operands
from .core import TensorRandomOperandMixin, handle_array


class TensorNormal(operands.Normal, TensorRandomOperandMixin):
    __slots__ = '_loc', '_scale', '_size'
    _input_fields_ = ['_loc', '_scale']

    def __init__(self, size=None, state=None, dtype=None, gpu=None, **kw):
        dtype = np.dtype(dtype) if dtype is not None else dtype
        super(TensorNormal, self).__init__(_size=size, _state=state, _dtype=dtype,
                                           _gpu=gpu, **kw)

    def __call__(self, loc, scale, chunks=None):
        return self.new_tensor([loc, scale], None, raw_chunks=chunks)


def normal(random_state, loc=0.0, scale=1.0, size=None, chunks=None, gpu=None, **kw):
    r"""
    Draw random samples from a normal (Gaussian) distribution.

    The probability density function of the normal distribution, first
    derived by De Moivre and 200 years later by both Gauss and Laplace
    independently [2]_, is often called the bell curve because of
    its characteristic shape (see the example below).

    The normal distributions occurs often in nature.  For example, it
    describes the commonly occurring distribution of samples influenced
    by a large number of tiny, random disturbances, each with its own
    unique distribution [2]_.

    Parameters
    ----------
    loc : float or array_like of floats
        Mean ("centre") of the distribution.
    scale : float or array_like of floats
        Standard deviation (spread or "width") of the distribution.
    size : int or tuple of ints, optional
        Output shape.  If the given shape is, e.g., ``(m, n, k)``, then
        ``m * n * k`` samples are drawn.  If size is ``None`` (default),
        a single value is returned if ``loc`` and ``scale`` are both scalars.
        Otherwise, ``mt.broadcast(loc, scale).size`` samples are drawn.
    chunks : int or tuple of int or tuple of ints, optional
        Desired chunk size on each dimension
    gpu : bool, optional
        Allocate the tensor on GPU if True, False as default

    Returns
    -------
    out : Tensor or scalar
        Drawn samples from the parameterized normal distribution.

    See Also
    --------
    scipy.stats.norm : probability density function, distribution or
        cumulative density function, etc.

    Notes
    -----
    The probability density for the Gaussian distribution is

    .. math:: p(x) = \frac{1}{\sqrt{ 2 \pi \sigma^2 }}
                     e^{ - \frac{ (x - \mu)^2 } {2 \sigma^2} },

    where :math:`\mu` is the mean and :math:`\sigma` the standard
    deviation. The square of the standard deviation, :math:`\sigma^2`,
    is called the variance.

    The function has its peak at the mean, and its "spread" increases with
    the standard deviation (the function reaches 0.607 times its maximum at
    :math:`x + \sigma` and :math:`x - \sigma` [2]_).  This implies that
    `numpy.random.normal` is more likely to return samples lying close to
    the mean, rather than those far away.

    References
    ----------
    .. [1] Wikipedia, "Normal distribution",
           http://en.wikipedia.org/wiki/Normal_distribution
    .. [2] P. R. Peebles Jr., "Central Limit Theorem" in "Probability,
           Random Variables and Random Signal Principles", 4th ed., 2001,
           pp. 51, 51, 125.

    Examples
    --------
    Draw samples from the distribution:

    >>> import mars.tensor as mt

    >>> mu, sigma = 0, 0.1 # mean and standard deviation
    >>> s = mt.random.normal(mu, sigma, 1000)

    Verify the mean and the variance:

    >>> (abs(mu - mt.mean(s)) < 0.01).execute()
    True

    >>> (abs(sigma - mt.std(s, ddof=1)) < 0.01).execute()
    True

    Display the histogram of the samples, along with
    the probability density function:

    >>> import matplotlib.pyplot as plt
    >>> count, bins, ignored = plt.hist(s.execute(), 30, normed=True)
    >>> plt.plot(bins, (1/(sigma * mt.sqrt(2 * mt.pi)) *
    ...                mt.exp( - (bins - mu)**2 / (2 * sigma**2) )).execute(),
    ...          linewidth=2, color='r')
    >>> plt.show()
    """
    if 'dtype' not in kw:
        kw['dtype'] = np.random.RandomState().normal(
            handle_array(loc), handle_array(scale), size=(0,)).dtype
    size = random_state._handle_size(size)
    op = TensorNormal(size=size, state=random_state._state, gpu=gpu, **kw)
    return op(loc, scale, chunks=chunks)
