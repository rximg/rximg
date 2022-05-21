from .np_enums import *
import numpy as np
from numpy import ndarray
from typing import Tuple
from engine.decorator import rx_func,RETURN_TYPE

@rx_func()
def ufunc_reduce(array, axis, dtype:ENUM_CV_DTYPE, ):
    return np.ufunc.reduce(array, axis, dtype )

@rx_func()
def ufunc_accumulate(array, axis, dtype:ENUM_CV_DTYPE, ):
    return np.ufunc.accumulate(array, axis, dtype, )

@rx_func()
def ufunc_reduceat(array, indices, axis, ):
    return np.ufunc.reduceat(array, indices, axis, )

@rx_func()
def ufunc_at(a:ndarray, indices):
    return np.ufunc.at(a, indices)

@rx_func()
def add(x1:ndarray, x2:ndarray, ):
    return np.add(x1, x2, )

@rx_func()
def subtract(x1:ndarray, x2:ndarray, ):
    return np.subtract(x1, x2, )

@rx_func()
def multiply(x1:ndarray, x2:ndarray, ):
    return np.multiply(x1, x2, )

@rx_func()
def matmul(x1:ndarray, x2:ndarray, ):
    return np.matmul(x1, x2,)

@rx_func()
def divide(x1:ndarray, x2:ndarray, ):
    return np.divide(x1, x2, )

@rx_func()
def logaddexp(x1:ndarray, x2:ndarray, ):
    return np.logaddexp(x1, x2, )

@rx_func()
def logaddexp2(x1:ndarray, x2:ndarray, ):
    return np.logaddexp2(x1, x2, )

@rx_func()
def true_divide(x1:ndarray, x2:ndarray, ):
    return np.true_divide(x1, x2, )

@rx_func()
def floor_divide(x1:ndarray, x2:ndarray, ):
    return np.floor_divide(x1, x2, )

@rx_func()
def negative(x:ndarray, ):
    return np.negative(x, )

@rx_func()
def positive(x:ndarray, ):
    return np.positive(x, )

@rx_func()
def power(x1:ndarray, x2:ndarray, ):
    return np.power(x1, x2, )

@rx_func()
def float_power(x1:ndarray, x2:ndarray, ):
    return np.float_power(x1, x2, )

@rx_func()
def remainder(x1:ndarray, x2:ndarray, ):
    return np.remainder(x1, x2, )

@rx_func()
def mod(x1:ndarray, x2:ndarray, ):
    return np.mod(x1, x2, )

@rx_func()
def fmod(x1:ndarray, x2:ndarray, ):
    return np.fmod(x1, x2, )

@rx_func()
def divmod_(x1:ndarray, x2):
    return np.divmod(x1, x2)

@rx_func()
def absolute(x:ndarray, ):
    return np.absolute(x, )

@rx_func()
def fabs(x:ndarray, ):
    return np.fabs(x, )

@rx_func()
def rint(x:ndarray, ):
    return np.rint(x, )

@rx_func()
def sign(x:ndarray, ):
    return np.sign(x, )

@rx_func()
def heaviside(x1:ndarray, x2:ndarray, ):
    return np.heaviside(x1, x2, )

@rx_func()
def conj(x:ndarray, ):
    return np.conj(x, )

@rx_func()
def conjugate(x:ndarray, ):
    return np.conjugate(x, )

@rx_func()
def exp(x:ndarray, ):
    return np.exp(x, )

@rx_func()
def exp2(x:ndarray, ):
    return np.exp2(x, )

@rx_func()
def log(x:ndarray, ):
    return np.log(x, )

@rx_func()
def log2(x:ndarray, ):
    return np.log2(x, )

@rx_func()
def log10(x:ndarray, ):
    return np.log10(x, )

@rx_func()
def expm1(x:ndarray, ):
    return np.expm1(x, )

@rx_func()
def log1p(x:ndarray, ):
    return np.log1p(x, )

@rx_func()
def sqrt(x:ndarray, ):
    return np.sqrt(x, )

@rx_func()
def square(x:ndarray, ):
    return np.square(x, )

@rx_func()
def cbrt(x:ndarray, ):
    return np.cbrt(x, )

@rx_func()
def reciprocal(x:ndarray, ):
    return np.reciprocal(x, )

@rx_func()
def gcd(x1:ndarray, x2:ndarray, ):
    return np.gcd(x1, x2, )

@rx_func()
def lcm(x1:ndarray, x2:ndarray, ):
    return np.lcm(x1, x2, )

@rx_func()
def sin(x:ndarray, ):
    return np.sin(x, )

@rx_func()
def cos(x:ndarray, ):
    return np.cos(x, )

@rx_func()
def tan(x:ndarray, ):
    return np.tan(x, )

@rx_func()
def arcsin(x:ndarray, ):
    return np.arcsin(x, )

@rx_func()
def arccos(x:ndarray, ):
    return np.arccos(x, )

@rx_func()
def arctan(x:ndarray, ):
    return np.arctan(x, )

@rx_func()
def arctan2(x1:ndarray, x2:ndarray, ):
    return np.arctan2(x1, x2, )

@rx_func()
def hypot(x1:ndarray, x2:ndarray, ):
    return np.hypot(x1, x2, )

@rx_func()
def sinh(x:ndarray, ):
    return np.sinh(x, )

@rx_func()
def cosh(x:ndarray, ):
    return np.cosh(x, )

@rx_func()
def tanh(x:ndarray, ):
    return np.tanh(x, )

@rx_func()
def arcsinh(x:ndarray, ):
    return np.arcsinh(x, )

@rx_func()
def arccosh(x:ndarray, ):
    return np.arccosh(x, )

@rx_func()
def arctanh(x:ndarray, ):
    return np.arctanh(x, )

@rx_func()
def degrees(x:ndarray, ):
    return np.degrees(x, )

@rx_func()
def radians(x:ndarray, ):
    return np.radians(x, )

@rx_func()
def deg2rad(x:ndarray, ):
    return np.deg2rad(x, )

@rx_func()
def rad2deg(x:ndarray, ):
    return np.rad2deg(x, )

@rx_func()
def bitwise_and(x1:ndarray, x2:ndarray, ):
    return np.bitwise_and(x1, x2, )

@rx_func()
def bitwise_or(x1:ndarray, x2:ndarray, ):
    return np.bitwise_or(x1, x2, )

@rx_func()
def bitwise_xor(x1:ndarray, x2:ndarray, ):
    return np.bitwise_xor(x1, x2, )

@rx_func()
def invert(x:ndarray, ):
    return np.invert(x, )

@rx_func()
def left_shift(x1:ndarray, x2:ndarray, ):
    return np.left_shift(x1, x2, )

@rx_func()
def right_shift(x1:ndarray, x2:ndarray, ):
    return np.right_shift(x1, x2, )

@rx_func()
def greater(x1:ndarray, x2:ndarray, ):
    return np.greater(x1, x2, )

@rx_func()
def greater_equal(x1:ndarray, x2:ndarray, ):
    return np.greater_equal(x1, x2, )

@rx_func()
def less(x1:ndarray, x2:ndarray, ):
    return np.less(x1, x2, )

@rx_func()
def less_equal(x1:ndarray, x2:ndarray, ):
    return np.less_equal(x1, x2, )

@rx_func()
def not_equal(x1:ndarray, x2:ndarray, ):
    return np.not_equal(x1, x2, )

@rx_func()
def equal(x1:ndarray, x2:ndarray, ):
    return np.equal(x1, x2, )

@rx_func()
def logical_and(x1:ndarray, x2:ndarray, ):
    return np.logical_and(x1, x2, )

@rx_func()
def logical_or(x1:ndarray, x2:ndarray, ):
    return np.logical_or(x1, x2, )

@rx_func()
def logical_xor(x1:ndarray, x2:ndarray, ):
    return np.logical_xor(x1, x2, )

@rx_func()
def logical_not(x:ndarray, ):
    return np.logical_not(x, )

@rx_func()
def maximum(x1:ndarray, x2:ndarray, ):
    return np.maximum(x1, x2, )

@rx_func()
def minimum(x1:ndarray, x2:ndarray, ):
    return np.minimum(x1, x2, )

@rx_func()
def fmax(x1:ndarray, x2:ndarray, ):
    return np.fmax(x1, x2, )

@rx_func()
def fmin(x1:ndarray, x2:ndarray, ):
    return np.fmin(x1, x2, )

@rx_func()
def isfinite(x:ndarray, ):
    return np.isfinite(x, )

@rx_func()
def isinf(x:ndarray, ):
    return np.isinf(x, )

@rx_func()
def isnan(x:ndarray, ):
    return np.isnan(x, )

@rx_func()
def isnat(x:ndarray, ):
    return np.isnat(x, )

@rx_func()
def fabs(x:ndarray, ):
    return np.fabs(x, )

@rx_func()
def signbit(x:ndarray, ):
    return np.signbit(x, )

@rx_func()
def copysign(x1:ndarray, x2:ndarray, ):
    return np.copysign(x1, x2, )

@rx_func()
def nextafter(x1:ndarray, x2:ndarray, ):
    return np.nextafter(x1, x2, )

@rx_func()
def spacing(x:ndarray, ):
    return np.spacing(x, )

@rx_func()
def modf(x):
    return np.modf()

@rx_func()
def ldexp(x1:ndarray, x2:ndarray, ):
    return np.ldexp(x1, x2, )

@rx_func()
def frexp(x):
    return np.frexp(x)

@rx_func()
def fmod(x1:ndarray, x2:ndarray, ):
    return np.fmod(x1, x2, )

@rx_func()
def floor(x:ndarray, ):
    return np.floor(x, )

@rx_func()
def ceil(x:ndarray, ):
    return np.ceil(x, )

@rx_func()
def trunc(x:ndarray, ):
    return np.trunc(x, )

@rx_func()
def empty(shape:tuple, dtype:ENUM_CV_DTYPE):
    return np.empty(shape, dtype, )

@rx_func()
def empty_like(prototype, dtype, order, subok, ):
    return np.empty_like(prototype, dtype, order, subok, )

@rx_func()
def eye(N, M, k, dtype, ):
    return np.eye(N, M, k, dtype, )

@rx_func()
def identity(n, dtype, ):
    return np.identity(n, dtype, )

@rx_func()
def ones(shape:tuple, dtype:ENUM_CV_DTYPE):
    return np.ones(shape, dtype, )

@rx_func()
def ones_like(a:ndarray, dtype, ):
    return np.ones_like(a, dtype, )

@rx_func()
def zeros(shape:tuple, dtype:ENUM_CV_DTYPE):
    return np.zeros(shape, dtype, )

@rx_func()
def zeros_like(a:ndarray, dtype, ):
    return np.zeros_like(a, dtype, )

@rx_func()
def full(shape:tuple, fill_value, dtype:ENUM_CV_DTYPE):
    return np.full(shape, fill_value, dtype, )

@rx_func()
def full_like(a:ndarray, fill_value, dtype, order, ):
    return np.full_like(a, fill_value, dtype, order, )

@rx_func()
def array(object, dtype, copy, order, subok, ):
    return np.array(object, dtype, copy, order, subok, )

@rx_func()
def asarray(a:ndarray, dtype:ENUM_CV_DTYPE):
    return np.asarray(a, dtype, )

@rx_func()
def asanyarray(a:ndarray, dtype:ENUM_CV_DTYPE):
    return np.asanyarray(a, dtype, )

@rx_func()
def ascontiguousarray(a:ndarray, dtype, ):
    return np.ascontiguousarray(a, dtype, )

@rx_func()
def asmatrix(data:ndarray, dtype):
    return np.asmatrix(data, dtype)

@rx_func()
def copy(a:ndarray, order, ):
    return np.copy(a, order, )

@rx_func()
def arange(start, stop, step, dtype, ):
    return np.arange(start, stop, step, dtype, )

@rx_func()
def linspace(start, stop, num, endpoint, ):
    return np.linspace(start, stop, num, endpoint, )

@rx_func()
def diag(v, k):
    return np.diag(v, k)

@rx_func()
def diagflat(v, k):
    return np.diagflat(v, k)

@rx_func()
def tri(N, M, k, dtype, ):
    return np.tri(N, M, k, dtype, )

@rx_func()
def tril(m, k):
    return np.tril(m, k)

@rx_func()
def triu(m, k):
    return np.triu(m, k)

@rx_func()
def vander(x:ndarray, N, increasing:bool):
    return np.vander(x, N, increasing)

@rx_func()
def mat(data:ndarray, dtype):
    return np.mat(data, dtype)

@rx_func()
def copyto(dst, src,):
    return np.copyto(dst, src,)

@rx_func()
def shape(a):
    return np.shape(a)

@rx_func()
def reshape(a:ndarray, newshape:tuple, ):
    return np.reshape(a, newshape, )

@rx_func()
def ravel(a:ndarray, ):
    return np.ravel(a, )

@rx_func()
def ndarray_flatten():
    return np.ndarray.flatten()

@rx_func()
def moveaxis(a:ndarray, source, destination):
    return np.moveaxis(a, source, destination)

@rx_func()
def rollaxis(a:ndarray, axis, start):
    return np.rollaxis(a, axis, start)

@rx_func()
def swapaxes(a:ndarray, axis1, axis2):
    return np.swapaxes(a, axis1, axis2)

@rx_func()
def transpose(a:ndarray, axes):
    return np.transpose(a, axes)

@rx_func()
def atleast_1d(*arys):
    return np.atleast_1d(*arys)

@rx_func()
def atleast_2d(*arys):
    return np.atleast_2d(*arys)

@rx_func()
def atleast_3d(*arys):
    return np.atleast_3d(*arys)

@rx_func()
def broadcast_to(array, shape:tuple, ):
    return np.broadcast_to(array, shape, )

@rx_func()
def broadcast_arrays(*args, ):
    return np.broadcast_arrays(*args, )

@rx_func()
def expand_dims(a:ndarray, axis):
    return np.expand_dims(a, axis)

@rx_func()
def squeeze(a:ndarray, axis):
    return np.squeeze(a, axis)

@rx_func()
def asarray(a:ndarray, dtype:ENUM_CV_DTYPE):
    return np.asarray(a, dtype, )

@rx_func()
def asanyarray(a:ndarray, dtype:ENUM_CV_DTYPE):
    return np.asanyarray(a, dtype, )

@rx_func()
def asmatrix(data:ndarray, dtype):
    return np.asmatrix(data, dtype)

@rx_func()
def asfarray(a:ndarray, dtype):
    return np.asfarray(a, dtype)

@rx_func()
def asfortranarray(a:ndarray, dtype, ):
    return np.asfortranarray(a, dtype, )

@rx_func()
def ascontiguousarray(a:ndarray, dtype, ):
    return np.ascontiguousarray(a, dtype, )

@rx_func()
def asarray_chkfinite(a:ndarray, dtype, ):
    return np.asarray_chkfinite(a, dtype, )

@rx_func()
def asscalar(a):
    return np.asscalar(a)

@rx_func()
def require(a:ndarray, dtype, requirements, ):
    return np.require(a, dtype, requirements, )

@rx_func()
def concatenate(axis, dtype, ):
    return np.concatenate(axis=axis, dtype=dtype)

@rx_func()
def stack(arrays, axis, ):
    return np.stack(arrays, axis, )

@rx_func()
def block(arrays):
    return np.block(arrays)

@rx_func()
def vstack(tup):
    return np.vstack(tup)

@rx_func()
def hstack(tup):
    return np.hstack(tup)

@rx_func()
def dstack(tup):
    return np.dstack(tup)

@rx_func()
def column_stack(tup):
    return np.column_stack(tup)

@rx_func()
def row_stack(tup):
    return np.row_stack(tup)

@rx_func()
def split(ary, indices_or_sections, axis):
    return np.split(ary, indices_or_sections, axis)

@rx_func()
def array_split(ary, indices_or_sections, axis):
    return np.array_split(ary, indices_or_sections, axis)

@rx_func()
def dsplit(ary, indices_or_sections):
    return np.dsplit(ary, indices_or_sections)

@rx_func()
def hsplit(ary, indices_or_sections):
    return np.hsplit(ary, indices_or_sections)

@rx_func()
def vsplit(ary, indices_or_sections):
    return np.vsplit(ary, indices_or_sections)

@rx_func()
def tile(A, reps):
    return np.tile(A, reps)

@rx_func()
def repeat(a:ndarray, repeats, axis):
    return np.repeat(a, repeats, axis)

@rx_func()
def delete(arr, obj, axis):
    return np.delete(arr, obj, axis)

@rx_func()
def insert(arr, obj, values, axis):
    return np.insert(arr, obj, values, axis)

@rx_func()
def append(arr, values, axis):
    return np.append(arr, values, axis)

@rx_func()
def resize(a:ndarray, new_shape):
    return np.resize(a, new_shape)

@rx_func()
def unique(ar, return_index:ndarray, return_inverse, ):
    return np.unique(ar, return_index, return_inverse, )

@rx_func()
def flip(m, axis):
    return np.flip(m, axis)

@rx_func()
def fliplr(m):
    return np.fliplr(m)

@rx_func()
def flipud(m):
    return np.flipud(m)

@rx_func()
def reshape(a:ndarray, newshape:tuple, ):
    return np.reshape(a, newshape, )

@rx_func()
def roll(a:ndarray, shift, axis):
    return np.roll(a, shift, axis)

@rx_func()
def rot90(m, k, axes):
    return np.rot90(m, k, axes)

@rx_func()
def bitwise_and(x1:ndarray, x2:ndarray, ):
    return np.bitwise_and(x1, x2, )

@rx_func()
def bitwise_or(x1:ndarray, x2:ndarray, ):
    return np.bitwise_or(x1, x2, )

@rx_func()
def bitwise_xor(x1:ndarray, x2:ndarray, ):
    return np.bitwise_xor(x1, x2, )

@rx_func()
def invert(x:ndarray, ):
    return np.invert(x, )

@rx_func()
def left_shift(x1:ndarray, x2:ndarray, ):
    return np.left_shift(x1, x2, )

@rx_func()
def right_shift(x1:ndarray, x2:ndarray, ):
    return np.right_shift(x1, x2, )

@rx_func()
def fft(a:ndarray, n:int=None, axis:int=-1, norm:ENUM_CV_FFT_NORM=ENUM_CV_FFT_NORM.default):
    return np.fft.fft(a, n, axis, norm)

@rx_func()
def ifft(a:ndarray, n:int=None, axis:int=-1, norm:ENUM_CV_FFT_NORM=ENUM_CV_FFT_NORM.default):
    return np.fft.ifft(a, n, axis, norm)

@rx_func()
def fft2(a:ndarray, s:Tuple=None, axes:Tuple=(-2,-1), norm:ENUM_CV_FFT_NORM=ENUM_CV_FFT_NORM.default):
    return np.fft.fft2(a, s, axes, norm)

@rx_func()
def ifft2(a:ndarray, s:Tuple=None, axes:Tuple=(-2,-1), norm:ENUM_CV_FFT_NORM=ENUM_CV_FFT_NORM.default):
    return np.fft.ifft2(a, s, axes, norm)

@rx_func()
def fftn(a:ndarray, s:Tuple=None, axes:Tuple=(-2,-1), norm:ENUM_CV_FFT_NORM=ENUM_CV_FFT_NORM.default):
    return np.fft.fftn(a, s, axes, norm)

@rx_func()
def ifftn(a:ndarray, s:Tuple=None, axes:Tuple=(-2,-1), norm:ENUM_CV_FFT_NORM=ENUM_CV_FFT_NORM.default):
    return np.fft.ifftn(a, s, axes, norm)


@rx_func()
def fftfreq(n:ndarray, d:int=1.0):
    return np.fft.fftfreq(n, d)

@rx_func()
def rfftfreq(n:ndarray, d:int=1.0):
    return np.fft.rfftfreq(n, d)

@rx_func()
def fftshift(x:ndarray, axes:Tuple=None):
    return np.fft.fftshift(x, axes)

@rx_func()
def ifftshift(x:ndarray, axes:Tuple=None):
    return np.fft.ifftshift(x, axes)

@rx_func()
def dot(a:ndarray, b:ndarray, ):
    return np.dot(a, b, )

@rx_func()
# def linalg_multi_dot(arrays, *, ):
    # return np.linalg.multi_dot(arrays, *, )

@rx_func()
def vdot(a:ndarray, b:ndarray, ):
    return np.vdot(a, b, )

@rx_func()
def inner(a:ndarray, b:ndarray, ):
    return np.inner(a, b, )

@rx_func()
def outer(a:ndarray, b:ndarray, ):
    return np.outer(a, b, )

@rx_func()
def matmul(x1:ndarray, x2:ndarray, ):
    return np.matmul(x1, x2,)

@rx_func()
def tensordot(a:ndarray, b:ndarray, axes):
    return np.tensordot(a, b, axes)

@rx_func()
def einsum(subscripts, *operands, ):
    return np.einsum(subscripts, *operands )

@rx_func()
# def einsum_path(subscripts, *operands, optimize):
#     return np.einsum_path(subscripts, *operands, optimize)

@rx_func()
def linalg_matrix_power(a:ndarray, n):
    return np.linalg.matrix_power(a, n)

@rx_func()
def kron(a:ndarray, b):
    return np.kron(a, b)

@rx_func()
def linalg_cholesky(a):
    return np.linalg.cholesky(a)

@rx_func()
def linalg_qr(a:ndarray, mode):
    return np.linalg.qr(a, mode)

@rx_func()
def linalg_svd(a:ndarray, full_matrices, compute_uv, ):
    return np.linalg.svd(a, full_matrices, compute_uv, )

@rx_func()
def linalg_eig(a):
    return np.linalg.eig(a)

@rx_func()
def linalg_eigh(a:ndarray, UPLO):
    return np.linalg.eigh(a, UPLO)

@rx_func()
def linalg_eigvals(a):
    return np.linalg.eigvals(a)

@rx_func()
def linalg_eigvalsh(a:ndarray, UPLO):
    return np.linalg.eigvalsh(a, UPLO)

@rx_func()
def linalg_norm(x:ndarray, ord, axis, keepdims):
    return np.linalg.norm(x, ord, axis, keepdims)

@rx_func()
def linalg_cond(x:ndarray, p):
    return np.linalg.cond(x, p)

@rx_func()
def linalg_det(a):
    return np.linalg.det(a)

@rx_func()
def linalg_matrix_rank(A, tol, hermitian):
    return np.linalg.matrix_rank(A, tol, hermitian)

@rx_func()
def linalg_slogdet(a):
    return np.linalg.slogdet(a)

@rx_func()
def trace(a:ndarray, offset, axis1, axis2, dtype, ):
    return np.trace(a, offset, axis1, axis2, dtype, )

@rx_func()
def linalg_solve(a:ndarray, b):
    return np.linalg.solve(a, b)

@rx_func()
def linalg_tensorsolve(a:ndarray, b:ndarray, axes):
    return np.linalg.tensorsolve(a, b, axes)

@rx_func()
def linalg_lstsq(a:ndarray, b:ndarray, rcond):
    return np.linalg.lstsq(a, b, rcond)

@rx_func()
def linalg_inv(a):
    return np.linalg.inv(a)

@rx_func()
def linalg_pinv(a:ndarray, rcond, hermitian):
    return np.linalg.pinv(a, rcond, hermitian)

@rx_func()
def linalg_tensorinv(a:ndarray, ind):
    return np.linalg.tensorinv(a, ind)

@rx_func()
def all(a:ndarray, axis, out, keepdims, where):
    return np.all(a, axis, out, keepdims, where)

@rx_func()
def any(a:ndarray, axis, out, keepdims, where):
    return np.any(a, axis, out, keepdims, where)

@rx_func()
def isfinite(x:ndarray, ):
    return np.isfinite(x, )

@rx_func()
def isinf(x:ndarray, ):
    return np.isinf(x, )

@rx_func()
def isnan(x:ndarray, ):
    return np.isnan(x, )

@rx_func()
def isnat(x:ndarray, ):
    return np.isnat(x, )

@rx_func()
def isneginf(x:ndarray, ):
    return np.isneginf(x, )

@rx_func()
def isposinf(x:ndarray, ):
    return np.isposinf(x, )

@rx_func()
def iscomplex(x):
    return np.iscomplex(x)

@rx_func()
def iscomplexobj(x):
    return np.iscomplexobj(x)

@rx_func()
def isfortran(a):
    return np.isfortran(a)

@rx_func()
def isreal(x):
    return np.isreal(x)

@rx_func()
def isrealobj(x):
    return np.isrealobj(x)

@rx_func()
def isscalar(element):
    return np.isscalar(element)

@rx_func()
def logical_and(x1:ndarray, x2:ndarray, ):
    return np.logical_and(x1, x2, )

@rx_func()
def logical_or(x1:ndarray, x2:ndarray, ):
    return np.logical_or(x1, x2, )

@rx_func()
def logical_not(x:ndarray, ):
    return np.logical_not(x, )

@rx_func()
def logical_xor(x1:ndarray, x2:ndarray, ):
    return np.logical_xor(x1, x2, )

@rx_func()
def allclose(a:ndarray, b:ndarray, rtol, atol, equal_nan):
    return np.allclose(a, b, rtol, atol, equal_nan)

@rx_func()
def isclose(a:ndarray, b:ndarray, rtol, atol, equal_nan):
    return np.isclose(a, b, rtol, atol, equal_nan)

@rx_func()
def array_equal(a1, a2, equal_nan):
    return np.array_equal(a1, a2, equal_nan)

@rx_func()
def array_equiv(a1, a2):
    return np.array_equiv(a1, a2)

@rx_func()
def greater(x1:ndarray, x2:ndarray, ):
    return np.greater(x1, x2, )

@rx_func()
def greater_equal(x1:ndarray, x2:ndarray, ):
    return np.greater_equal(x1, x2, )

@rx_func()
def less(x1:ndarray, x2:ndarray, ):
    return np.less(x1, x2, )

@rx_func()
def less_equal(x1:ndarray, x2:ndarray, ):
    return np.less_equal(x1, x2, )

@rx_func()
def equal(x1:ndarray, x2:ndarray, ):
    return np.equal(x1, x2, )

@rx_func()
def not_equal(x1:ndarray, x2:ndarray, ):
    return np.not_equal(x1, x2, )
