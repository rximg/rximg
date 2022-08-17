from .cv2_enums import *
from enum import IntEnum
from engine.decorators import rx_func
import typing
from typing import Any, Tuple
from numpy.typing import NDArray
import numpy as np
import cv2
import os.path as osp
import os
import pdb
import requests
import sys
sys.path.append('.')
# class CVENUM(IntEnum):

#     default = 1


# class INTENUM(object):
#     def __init__(self,name:str,choice:typing.Sequence,default=None) -> None:
#         super().__init__()
#         self.choice=choice
#         if len(self.choice)==0:
#             raise ValueError('None choices:{}'.format(choice))
#         if default:
#             self.default=default
#         else:
#             self.default = choice[0]
#         self.__name__ = name



# def create_int_num(name:str,choice:typing.Sequence,default=None):
#     if len(choice)==0:
#         raise ValueError('None choices:{}'.format(choice))
#     if not default:
#         default = choice[0]
#     return type(name,(INTENUM,),{'choice':choice,'default':default,})


class ENUM_CV_DEPTH(CVINTENUM):
    default = -1
    CV_8U = 0
    CV_16U = 2
    CV_16S = 3
    CV_32F = 5
    CV_64F = 6
    # ["","","CV_16S","CV_32F","CV64F"]


# @view
# def imshow(mat:NDArray) -> typing.Any:
#     """    'imshow(winname, mat) -> None
# .   @brief Displays an image in the specified window.
# .
# .   The function imshow displays an image in the specified window. If the window was created with the
# .   cv::WINDOW_AUTOSIZE flag, the image is shown with its original size, however it is still limited by the screen resolution.
# .   Otherwise, the image is scaled to fit the window. The function may scale the image, depending on its depth:
# .
# .   -   If the image is 8-bit unsigned, it is displayed as is.
# .   -   If the image is 16-bit unsigned or 32-bit integer, the pixels are divided by 256. That is, the
# .       value range [0,255\\*256] is mapped to [0,255].
# .   -   If the image is 32-bit or 64-bit floating-point, the pixel values are multiplied by 255. That is, the
# .       value range [0,1] is mapped to [0,255].
# .
# .   If window was created with OpenGL support, cv::imshow also support ogl::Buffer , ogl::Texture2D and
# .   cuda::GpuMat as input.
# .
# .   If the window was not created before this function, it is assumed creating a window with cv::WINDOW_AUTOSIZE.
# .
# .   If you need to show an image that is bigger than the screen resolution, you will need to call namedWindow("", WINDOW_NORMAL) before the imshow.
# .
# .   @note This function should be followed by cv::waitKey function which displays the image for specified
# .   milliseconds. Otherwise, it won't display the image. For example, **waitKey(0)** will display the window
# .   infinitely until any keypress (it is suitable for image display). **waitKey(25)** will display a frame
# .   for 25 ms, after which display will be automatically closed. (If you put it in a loop to read
# .   videos, it will display the video frame-by-frame)
# .
# .   @note
# .
# .   [__Windows Backend Only__] Pressing Ctrl+C will copy the image to the clipboard.
# .
# .   [__Windows Backend Only__] Pressing Ctrl+S will show a dialog to save the image.
# .
# .   @param winname Name of the window.
# .   @param mat Image to be shown.'

#     """
#     imname = str(id(mat))+'.png'
#     cv2.imwrite('./static/result/'+ imname,mat)
#     return imname
@rx_func()
def cvtColor(src: NDArray, code: ENUM_CV_ColorConversionCodes, dstCn: int = 0) -> np.ndarray:
    """    'cvtColor(src:NDArray, code[, dst[, dstCn]]) -> dst
.   @brief Converts an image from one color space to another.
.   
.   The function converts an input image from one color space to another. In case of a transformation
.   to-from RGB color space, the order of the channels should be specified explicitly (RGB or BGR). Note
.   that the default color format in OpenCV is often referred to as RGB but it is actually BGR (the
.   bytes are reversed). So the first byte in a standard (24-bit) color image will be an 8-bit Blue
.   component, the second byte will be Green, and the third byte will be Red. The fourth, fifth, and
.   sixth bytes would then be the second pixel (Blue, then Green, then Red), and so on.
.   
.   The conventional ranges for R, G, and B channel values are:
.   -   0 to 255 for CV_8U images
.   -   0 to 65535 for CV_16U images
.   -   0 to 1 for CV_32F images
.   
.   In case of linear transformations, the range does not matter. But in case of a non-linear
.   transformation, an input RGB image should be normalized to the proper value range to get the correct
.   results, for example, for RGB \\f$\\rightarrow\\f$ L\\*u\\*v\\* transformation. For example, if you have a
.   32-bit floating-point image directly converted from an 8-bit image without any scaling, then it will
.   have the 0..255 value range instead of 0..1 assumed by the function. So, before calling #cvtColor ,
.   you need first to scale the image down:
.   @code
.       img *= 1./255;
.       cvtColor(img:NDArray, img:NDArray, COLOR_BGR2Luv);
.   @endcode
.   If you use #cvtColor with 8-bit images, the conversion will have some information lost. For many
.   applications, this will not be noticeable but it is recommended to use 32-bit images in applications
.   that need the full range of colors or that convert an image before an operation and then convert
.   back.
.   
.   If conversion adds the alpha channel, its value will set to the maximum of corresponding channel
.   range: 255 for CV_8U, 65535 for CV_16U, 1 for CV_32F.
.   
.   @param src input image: 8-bit unsigned, 16-bit unsigned ( CV_16UC... ), or single-precision
.   floating-point.
.   @param dst output image of the same size and depth as src.
.   @param code color space conversion code (see #ColorConversionCodes).
.   @param dstCn number of channels in the destination image; if the parameter is 0, the number of the
.   channels is derived automatically from src and code.
.   
.   @see @ref imgproc_color_conversions'

    """
    print("$$cvtColor", code)
    return cv2.cvtColor(src=src, code=code, dstCn=dstCn)


@rx_func()
def imread(filename: str, flags: ENUM_CV_ImreadModes = ENUM_CV_ImreadModes.default) -> NDArray:
    """    'imread(filename[, flags]) -> retval
.   @brief Loads an image from a file.
.   
.   @anchor imread
.   
.   The function imread loads an image from the specified file and returns it. If the image cannot be
.   read (because of missing file, improper permissions, unsupported or invalid format), the function
.   returns an empty matrix ( Mat::data==NULL ).
.   
.   Currently, the following file formats are supported:
.   
.   -   Windows bitmaps - \\*.bmp, \\*.dib (always supported)
.   -   JPEG files - \\*.jpeg, \\*.jpg, \\*.jpe (see the *Note* section)
.   -   JPEG 2000 files - \\*.jp2 (see the *Note* section)
.   -   Portable Network Graphics - \\*.png (see the *Note* section)
.   -   WebP - \\*.webp (see the *Note* section)
.   -   Portable image format - \\*.pbm, \\*.pgm, \\*.ppm \\*.pxm, \\*.pnm (always supported)
.   -   PFM files - \\*.pfm (see the *Note* section)
.   -   Sun rasters - \\*.sr, \\*.ras (always supported)
.   -   TIFF files - \\*.tiff, \\*.tif (see the *Note* section)
.   -   OpenEXR Image files - \\*.exr (see the *Note* section)
.   -   Radiance HDR - \\*.hdr, \\*.pic (always supported)
.   -   Raster and Vector geospatial data supported by GDAL (see the *Note* section)
.   
.   @note
.   -   The function determines the type of an image by the content, not by the file extension.
.   -   In the case of color images, the decoded images will have the channels stored in **B G R** order.
.   -   When using IMREAD_GRAYSCALE, the codec\'s internal grayscale conversion will be used, if available.
.       Results may differ to the output of cvtColor()
.   -   On Microsoft Windows\\* OS and MacOSX\\*, the codecs shipped with an OpenCV image (libjpeg,
.       libpng, libtiff, and libjasper) are used by default. So, OpenCV can always read JPEGs, PNGs,
.       and TIFFs. On MacOSX, there is also an option to use native MacOSX image readers. But beware
.       that currently these native image loaders give images with different pixel values because of
.       the color management embedded into MacOSX.
.   -   On Linux\\*, BSD flavors and other Unix-like open-source operating systems, OpenCV looks for
.       codecs supplied with an OS image. Install the relevant packages (do not forget the development
.       files, for example, "libjpeg-dev", in Debian\\* and Ubuntu\\*) to get the codec support or turn
.       on the OPENCV_BUILD_3RDPARTY_LIBS flag in CMake.
.   -   In the case you set *WITH_GDAL* flag to true in CMake and @ref IMREAD_LOAD_GDAL to load the image,
.       then the [GDAL](http://www.gdal.org) driver will be used in order to decode the image, supporting
.       the following formats: [Raster](http://www.gdal.org/formats_list.html),
.       [Vector](http://www.gdal.org/ogr_formats.html).
.   -   If EXIF information is embedded in the image file, the EXIF orientation will be taken into account
.       and thus the image will be rotated accordingly except if the flags @ref IMREAD_IGNORE_ORIENTATION
.       or @ref IMREAD_UNCHANGED are passed.
.   -   Use the IMREAD_UNCHANGED flag to keep the floating point values from PFM image.
.   -   By default number of pixels must be less than 2^30. Limit can be set using system
.       variable OPENCV_IO_MAX_IMAGE_PIXELS
.   
.   @param filename Name of file to be loaded.
.   @param flags Flag that can take values of cv::ImreadModes'

    """
    # filename = osp.join('./cache',filename)
    assert isinstance(filename,str)
    if filename.lower().startswith("http://") or filename.lower().startswith("https://"):
        rep = requests.get(filename)
        image = np.asarray(bytearray(rep.content), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_UNCHANGED)
        return image
    # print(filename)
    return cv2.imread(filename=filename, flags=flags)


@rx_func()
def resize(src: NDArray, dsize: tuple, fx: int = 0, fy: int = 0,
           interpolation: ENUM_CV_InterpolationFlags = ENUM_CV_InterpolationFlags.INTER_LINEAR) -> NDArray:
    """    'resize(src:NDArray, dsize[, dst[, fx[, fy[, interpolation]]]]) -> dst
.   @brief Resizes an image.
.   
.   The function resize resizes the image src down to or up to the specified size. Note that the
.   initial dst type or size are not taken into account. Instead, the size and type are derived from
.   the `src`,`dsize`,`fx`, and `fy`. If you want to resize src so that it fits the pre-created dst,
.   you may call the function as follows:
.   @code
.       // explicitly specify dsize=dst.size(); fx and fy will be computed from that.
.       resize(src:NDArray, dst, dst.size(), 0, 0, interpolation);
.   @endcode
.   If you want to decimate the image by factor of 2 in each direction, you can call the function this
.   way:
.   @code
.       // specify fx and fy and let the function compute the destination image size.
.       resize(src:NDArray, dst, Size(), 0.5, 0.5, interpolation);
.   @endcode
.   To shrink an image, it will generally look best with #INTER_AREA interpolation, whereas to
.   enlarge an image, it will generally look best with c#INTER_CUBIC (slow) or #INTER_LINEAR
.   (faster but still looks OK).
.   
.   @param src input image.
.   @param dst output image; it has the size dsize (when it is non-zero) or the size computed from
.   src.size(), fx, and fy; the type of dst is the same as of src.
.   @param dsize output image size; if it equals zero, it is computed as:
.    \\f[\\texttt{dsize = Size(round(fx*src.cols), round(fy*src.rows))}\\f]
.    Either dsize or both fx and fy must be non-zero.
.   @param fx scale factor along the horizontal axis; when it equals 0, it is computed as
.   \\f[\\texttt{(double)dsize.width/src.cols}\\f]
.   @param fy scale factor along the vertical axis; when it equals 0, it is computed as
.   \\f[\\texttt{(double)dsize.height/src.rows}\\f]
.   @param interpolation interpolation method, see #InterpolationFlags
.   
.   @sa  warpAffine, warpPerspective, remap'

    """
    return cv2.resize(src=src, dsize=dsize, fx=fx, fy=fy, interpolation=interpolation)


@rx_func()
def putText(img: NDArray, text: str, org: tuple, fontFace: ENUM_CV_HersheyFonts,
            fontScale: float, color: tuple = (255, 255, 255), thickness: int = 1, lineType: int = 1, bottomLeftOrigin: bool = False) -> NDArray:
    """    'putText(img:NDArray, text, org, fontFace, fontScale, color[, thickness[, lineType[, bottomLeftOrigin]]]) -> img
.   @brief Draws a text string.
.   
.   The function cv::putText renders the specified text string in the image. Symbols that cannot be rendered
.   using the specified font are replaced by question marks. See #getTextSize for a text rendering code
.   example.
.   
.   @param img Image.
.   @param text Text string to be drawn.
.   @param org Bottom-left corner of the text string in the image.
.   @param fontFace Font type, see #HersheyFonts.
.   @param fontScale Font scale factor that is multiplied by the font-specific base size.
.   @param color Text color.
.   @param thickness Thickness of the lines used to draw a text.
.   @param lineType Line type. See #LineTypes
.   @param bottomLeftOrigin When true, the image data origin is at the bottom-left corner. Otherwise,
.   it is at the top-left corner.'

    """
    cv2.putText(img, text, org, fontFace, fontScale, color,
                thickness, lineType, bottomLeftOrigin)
    return img
# @rx_func()
# def  imwrite(filename:str, img:NDArray, params:tuple=()) -> typing.Any:
#     """    "imwrite(filename, img[, params]) -> retval
# .   @brief Saves an image to a specified file.
# .
# .   The function imwrite saves the image to the specified file. The image format is chosen based on the
# .   filename extension (see cv::imread for the list of extensions). In general, only 8-bit
# .   single-channel or 3-channel (with 'BGR' channel order) images
# .   can be saved using this function, with these exceptions:
# .
# .   - 16-bit unsigned (CV_16U) images can be saved in the case of PNG, JPEG 2000, and TIFF formats
# .   - 32-bit float (CV_32F) images can be saved in PFM, TIFF, OpenEXR, and Radiance HDR formats;
# .     3-channel (CV_32FC3) TIFF images will be saved using the LogLuv high dynamic range encoding
# .     (4 bytes per pixel)
# .   - PNG images with an alpha channel can be saved using this function. To do this, create
# .   8-bit (or 16-bit) 4-channel image BGRA, where the alpha channel goes last. Fully transparent pixels
# .   should have alpha set to 0, fully opaque pixels should have alpha set to 255/65535 (see the code sample below).
# .   - Multiple images (vector of Mat) can be saved in TIFF format (see the code sample below).
# .
# .   If the format, depth or channel order is different, use
# .   Mat::convertTo and cv::cvtColor to convert it before saving. Or, use the universal FileStorage I/O
# .   functions to save the image to XML or YAML format.
# .
# .   The sample below shows how to create a BGRA image, how to set custom compression parameters and save it to a PNG file.
# .   It also demonstrates how to save multiple images in a TIFF file:
# .   @include snippets/imgcodecs_imwrite.cpp
# .   @param filename Name of the file.
# .   @param img (Mat or vector of Mat) Image or Images to be saved.
# .   @param params Format-specific parameters encoded as pairs (paramId_1, paramValue_1, paramId_2, paramValue_2, ... .) see cv::ImwriteFlags"

#     """
#     pass


@rx_func()
def circle(img: NDArray, center: tuple, radius: int, color: tuple = (255, 255, 255),
           thickness: int = 1, lineType: int = 1, shift: int = 0) -> NDArray:
    # delete shift arg
    """    'circle(img:NDArray, center, radius, color[, thickness[, lineType[, shift]]]) -> img
.   @brief Draws a circle.
.   
.   The function cv::circle draws a simple or filled circle with a given center and radius.
.   @param img Image where the circle is drawn.
.   @param center Center of the circle.
.   @param radius Radius of the circle.
.   @param color Circle color.
.   @param thickness Thickness of the circle outline, if positive. Negative values, like #FILLED,
.   mean that a filled circle is to be drawn.
.   @param lineType Type of the circle boundary. See #LineTypes
.   @param shift Number of fractional bits in the coordinates of the center and in the radius value.'

    """
    # pdb.set_trace()
    cv2.circle(img, center, radius, color, thickness, lineType, shift)
    return img


@rx_func()
def line(img: NDArray, pt1: tuple, pt2: tuple, color: tuple = (255, 255, 255), thickness: int = 1, lineType: int = 1, shift: int = 0) -> NDArray:
    """    'line(img:NDArray, pt1, pt2, color[, thickness[, lineType[, shift]]]) -> img
.   @brief Draws a line segment connecting two points.
.   
.   The function line draws the line segment between pt1 and pt2 points in the image. The line is
.   clipped by the image boundaries. For non-antialiased lines with integer coordinates, the 8-connected
.   or 4-connected Bresenham algorithm is used. Thick lines are drawn with rounding endings. Antialiased
.   lines are drawn using Gaussian filtering.
.   
.   @param img Image.
.   @param pt1 First point of the line segment.
.   @param pt2 Second point of the line segment.
.   @param color Line color.
.   @param thickness Line thickness.
.   @param lineType Type of the line. See #LineTypes.
.   @param shift Number of fractional bits in the point coordinates.'

    """
    cv2.line(img, pt1, pt2, color, thickness, lineType, shift)
    return img


@rx_func()
def rectangle(img: NDArray, pt1: tuple, pt2: tuple, color: tuple = (255, 255, 255),
              thickness: int = 1, lineType: int = 1, shift: int = 0) -> NDArray:
    """    'rectangle(img:NDArray, pt1, pt2, color[, thickness[, lineType[, shift]]]) -> img
.   @brief Draws a simple, thick, or filled up-right rectangle.
.   
.   The function cv::rectangle draws a rectangle outline or a filled rectangle whose two opposite corners
.   are pt1 and pt2.
.   
.   @param img Image.
.   @param pt1 Vertex of the rectangle.
.   @param pt2 Vertex of the rectangle opposite to pt1 .
.   @param color Rectangle color or brightness (grayscale image).
.   @param thickness Thickness of lines that make up the rectangle. Negative values, like #FILLED,
.   mean that the function has to draw a filled rectangle.
.   @param lineType Type of the line. See #LineTypes
.   @param shift Number of fractional bits in the point coordinates.



rectangle(img:NDArray, rec, color[, thickness[, lineType[, shift]]]) -> img
.   @overload
.   
.   use `rec` parameter as alternative specification of the drawn rectangle: `r.tl() and
.   r.br()-Point(1,1)` are opposite corners'

    """

    cv2.rectangle(img, pt1, pt2, color, thickness, lineType, shift)
    return img


@rx_func()
def polylines(img: NDArray, pts: NDArray, isClosed: bool, color: tuple = (255, 255, 255), thickness: int = 1, lineType: int = 1, shift: int = 0) -> NDArray:
    """    'polylines(img:NDArray, pts, isClosed, color[, thickness[, lineType[, shift]]]) -> img
.   @brief Draws several polygonal curves.
.   
.   @param img Image.
.   @param pts Array of polygonal curves.
.   @param isClosed Flag indicating whether the drawn polylines are closed or not. If they are closed,
.   the function draws a line from the last vertex of each curve to its first vertex.
.   @param color Polyline color.
.   @param thickness Thickness of the polyline edges.
.   @param lineType Type of the line segments. See #LineTypes
.   @param shift Number of fractional bits in the vertex coordinates.
.   
.   The function cv::polylines draws one or more polygonal curves.'

    """
    return cv2.polylines(img, pts, isClosed, color, thickness, lineType, shift)


@rx_func()
def warpAffine(src: NDArray, M: NDArray, dsize: int,
               flags: ENUM_CV_InterpolationFlags = ENUM_CV_InterpolationFlags.INTER_LINEAR,
               borderMode: ENUM_CV_BorderTypes = ENUM_CV_BorderTypes.BORDER_CONSTANT,
               borderValue: tuple = (0, 0, 0)) -> NDArray:
    """    'warpAffine(src:NDArray, M, dsize[, dst[, flags[, borderMode[, borderValue]]]]) -> dst
.   @brief Applies an affine transformation to an image.
.   
.   The function warpAffine transforms the source image using the specified matrix:
.   
.   \\f[\\texttt{dst} (x,y) =  \\texttt{src} ( \\texttt{M} _{11} x +  \\texttt{M} _{12} y +  \\texttt{M} _{13}, \\texttt{M} _{21} x +  \\texttt{M} _{22} y +  \\texttt{M} _{23})\\f]
.   
.   when the flag #WARP_INVERSE_MAP is set. Otherwise, the transformation is first inverted
.   with #invertAffineTransform and then put in the formula above instead of M. The function cannot
.   operate in-place.
.   
.   @param src input image.
.   @param dst output image that has the size dsize and the same type as src .
.   @param M \\f$2\\times 3\\f$ transformation matrix.
.   @param dsize size of the output image.
.   @param flags combination of interpolation methods (see #InterpolationFlags) and the optional
.   flag #WARP_INVERSE_MAP that means that M is the inverse transformation (
.   \\f$\\texttt{dst}\\rightarrow\\texttt{src}\\f$ ).
.   @param borderMode pixel extrapolation method (see #BorderTypes); when
.   borderMode=#BORDER_TRANSPARENT, it means that the pixels in the destination image corresponding to
.   the "outliers" in the source image are not modified by the function.
.   @param borderValue value used in case of a constant border; by default, it is 0.
.   
.   @sa  warpPerspective, resize, remap, getRectSubPix, transform'

    """
    return cv2.warpAffine(src, M, dsize, flags, borderMode, borderValue)


@rx_func()
def threshold(src: NDArray, thresh: float, maxval: float, type: ENUM_CV_ThresholdTypes,) -> NDArray:
    """    "threshold(src:NDArray, thresh, maxval, type[, dst]) -> retval, dst
.   @brief Applies a fixed-level threshold to each array element.
.   
.   The function applies fixed-level thresholding to a multiple-channel array. The function is typically
.   used to get a bi-level (binary) image out of a grayscale image ( #compare could be also used for
.   this purpose) or for removing a noise, that is, filtering out pixels with too small or too large
.   values. There are several types of thresholding supported by the function. They are determined by
.   type parameter.
.   
.   Also, the special values #THRESH_OTSU or #THRESH_TRIANGLE may be combined with one of the
.   above values. In these cases, the function determines the optimal threshold value using the Otsu's
.   or Triangle algorithm and uses it instead of the specified thresh.
.   
.   @note Currently, the Otsu's and Triangle methods are implemented only for 8-bit single-channel images.
.   
.   @param src input array (multiple-channel, 8-bit or 32-bit floating point).
.   @param dst output array of the same size  and type and the same number of channels as src.
.   @param thresh threshold value.
.   @param maxval maximum value to use with the #THRESH_BINARY and #THRESH_BINARY_INV thresholding
.   types.
.   @param type thresholding type (see #ThresholdTypes).
.   @return the computed threshold value if Otsu's or Triangle methods used.
.   
.   @sa  adaptiveThreshold, findContours, compare, min, max"

    """
    # print(src.shape,thresh,maxval,type)
    return cv2.threshold(src=src, thresh=thresh, maxval=maxval, type=type)[1]


@rx_func()
def threshold_origin(src: NDArray, thresh: float, maxval: float, type: ENUM_CV_ThresholdTypes,) -> Tuple:
    """    "threshold(src:NDArray, thresh, maxval, type[, dst]) -> retval, dst
.   @brief Applies a fixed-level threshold to each array element.
.   
.   The function applies fixed-level thresholding to a multiple-channel array. The function is typically
.   used to get a bi-level (binary) image out of a grayscale image ( #compare could be also used for
.   this purpose) or for removing a noise, that is, filtering out pixels with too small or too large
.   values. There are several types of thresholding supported by the function. They are determined by
.   type parameter.
.   
.   Also, the special values #THRESH_OTSU or #THRESH_TRIANGLE may be combined with one of the
.   above values. In these cases, the function determines the optimal threshold value using the Otsu's
.   or Triangle algorithm and uses it instead of the specified thresh.
.   
.   @note Currently, the Otsu's and Triangle methods are implemented only for 8-bit single-channel images.
.   
.   @param src input array (multiple-channel, 8-bit or 32-bit floating point).
.   @param dst output array of the same size  and type and the same number of channels as src.
.   @param thresh threshold value.
.   @param maxval maximum value to use with the #THRESH_BINARY and #THRESH_BINARY_INV thresholding
.   types.
.   @param type thresholding type (see #ThresholdTypes).
.   @return the computed threshold value if Otsu's or Triangle methods used.
.   
.   @sa  adaptiveThreshold, findContours, compare, min, max"

    """
    # print(src.shape,thresh,maxval,type)
    return cv2.threshold(src, thresh, maxval, type)


@rx_func()
def fillConvexPoly(img: NDArray, points: NDArray, color: tuple = (255, 255, 255), lineType: int = 1, shift: int = 0) -> NDArray:
    """    'fillConvexPoly(img:NDArray, points, color[, lineType[, shift]]) -> img
.   @brief Fills a convex polygon.
.   
.   The function cv::fillConvexPoly draws a filled convex polygon. This function is much faster than the
.   function #fillPoly . It can fill not only convex polygons but any monotonic polygon without
.   self-intersections, that is, a polygon whose contour intersects every horizontal line (scan line)
.   twice at the most (though, its top-most and/or the bottom edge could be horizontal).
.   
.   @param img Image.
.   @param points Polygon vertices.
.   @param color Polygon color.
.   @param lineType Type of the polygon boundaries. See #LineTypes
.   @param shift Number of fractional bits in the vertex coordinates.'

    """
    return cv2.fillConvexPoly(img, points, color, lineType, shift)


@rx_func()
def GaussianBlur(src: NDArray, ksize: tuple, sigmaX: int=0, sigmaY: int = 0,
                 borderType: ENUM_CV_BorderTypes = ENUM_CV_BorderTypes.default) -> NDArray:
    """    "GaussianBlur(src:NDArray, ksize, sigmaX[, dst[, sigmaY[, borderType]]]) -> dst
.   @brief Blurs an image using a Gaussian filter.
.   
.   The function convolves the source image with the specified Gaussian kernel. In-place filtering is
.   supported.
.   
.   @param src input image; the image can have any number of channels, which are processed
.   independently, but the depth should be CV_8U, CV_16U, CV_16S, CV_32F or CV_64F.
.   @param dst output image of the same size and type as src.
.   @param ksize Gaussian kernel size. ksize.width and ksize.height can differ but they both must be
.   positive and odd. Or, they can be zero's and then they are computed from sigma.
.   @param sigmaX Gaussian kernel standard deviation in X direction.
.   @param sigmaY Gaussian kernel standard deviation in Y direction; if sigmaY is zero, it is set to be
.   equal to sigmaX, if both sigmas are zeros, they are computed from ksize.width and ksize.height,
.   respectively (see #getGaussianKernel for details); to fully control the result regardless of
.   possible future modifications of all this semantics, it is recommended to specify all of ksize,
.   sigmaX, and sigmaY.
.   @param borderType pixel extrapolation method, see #BorderTypes. #BORDER_WRAP is not supported.
.   
.   @sa  sepFilter2D, filter2D, blur, boxFilter, bilateralFilter, medianBlur"

    """
    return cv2.GaussianBlur(src, ksize, sigmaX, None, sigmaY, borderType)


@rx_func()
def boundingRect(array: NDArray) -> NDArray:
    """    'boundingRect(array) -> retval
.   @brief Calculates the up-right bounding rectangle of a point set or non-zero pixels of gray-scale image.
.   
.   The function calculates and returns the minimal up-right bounding rectangle for the specified point set or
.   non-zero pixels of gray-scale image.
.   
.   @param array Input gray-scale image or 2D point set, stored in std::vector or Mat.'

    """
    return cv2.boundingRect(array)


@rx_func()
def minAreaRect(points: NDArray) -> NDArray:
    """Finds a rotated rectangle of the minimum area enclosing the input 2D point set."""
    return cv2.minAreaRect(points=points)


@rx_func()
def minMaxLoc(src: NDArray, mask: NDArray = None) -> Tuple:
    """    'minMaxLoc(src[, mask]) -> minVal, maxVal, minLoc, maxLoc
.   @brief Finds the global minimum and maximum in an array.
.   
.   The function cv::minMaxLoc finds the minimum and maximum element values and their positions. The
.   extremums are searched across the whole array or, if mask is not an empty array, in the specified
.   array region.
.   
.   The function do not work with multi-channel arrays. If you need to find minimum or maximum
.   elements across all the channels, use Mat::reshape first to reinterpret the array as
.   single-channel. Or you may extract the particular channel using either extractImageCOI , or
.   mixChannels , or split .
.   @param src input single-channel array.
.   @param minVal pointer to the returned minimum value; NULL is used if not required.
.   @param maxVal pointer to the returned maximum value; NULL is used if not required.
.   @param minLoc pointer to the returned minimum location (in 2D case); NULL is used if not required.
.   @param maxLoc pointer to the returned maximum location (in 2D case); NULL is used if not required.
.   @param mask optional mask used to select a sub-array.
.   @sa max, min, compare, inRange, extractImageCOI, mixChannels, split, Mat::reshape'

    """
    return cv2.minMaxLoc(src, mask)


@rx_func()
def filter2D(src: NDArray,
             ddepth: ENUM_CV_DEPTH,
             kernel: NDArray,
             anchor: tuple = (-1, -1),
             delta: float = 0,
             borderType: ENUM_CV_BorderTypes = ENUM_CV_BorderTypes.default) -> NDArray:
    """    'filter2D(src:NDArray, ddepth, kernel[, dst[, anchor[, delta[, borderType]]]]) -> dst
.   @brief Convolves an image with the kernel.
.   
.   The function applies an arbitrary linear filter to an image. In-place operation is supported. When
.   the aperture is partially outside the image, the function interpolates outlier pixel values
.   according to the specified border mode.
.   
.   The function does actually compute correlation, not the convolution:
.   
.   \\f[\\texttt{dst} (x,y) =  \\sum _{ \\substack{0\\leq x\' < \\texttt{kernel.cols}\\\\{0\\leq y\' < \\texttt{kernel.rows}}}}  \\texttt{kernel} (x\',y\')* \\texttt{src} (x+x\'- \\texttt{anchor.x} ,y+y\'- \\texttt{anchor.y} )\\f]
.   
.   That is, the kernel is not mirrored around the anchor point. If you need a real convolution, flip
.   the kernel using #flip and set the new anchor to `(kernel.cols - anchor.x - 1, kernel.rows -
.   anchor.y - 1)`.
.   
.   The function uses the DFT-based algorithm in case of sufficiently large kernels (~`11 x 11` or
.   larger) and the direct algorithm for small kernels.
.   
.   @param src input image.
.   @param dst output image of the same size and the same number of channels as src.
.   @param ddepth desired depth of the destination image, see @ref filter_depths "combinations"
.   @param kernel convolution kernel (or rather a correlation kernel), a single-channel floating point
.   matrix; if you want to apply different kernels to different channels, split the image into
.   separate color planes using split and process them individually.
.   @param anchor anchor of the kernel that indicates the relative position of a filtered point within
.   the kernel; the anchor should lie within the kernel; default value (-1,-1) means that the anchor
.   is at the kernel center.
.   @param delta optional value added to the filtered pixels before storing them in dst.
.   @param borderType pixel extrapolation method, see #BorderTypes. #BORDER_WRAP is not supported.
.   @sa  sepFilter2D, dft, matchTemplate'

    """
    return cv2.filter2D(src, ddepth, kernel, None, anchor, delta, borderType)


@rx_func()
def Sobel(src: NDArray,
          ddepth: ENUM_CV_DEPTH,
          dx: int,
          dy: int,
          ksize: int = 3,
          scale: int = 1,
          delta: int = 1,
          borderType: ENUM_CV_BorderTypes = ENUM_CV_BorderTypes.default) -> NDArray:
    # dx dy [1,-1]
    """    'Sobel(src:NDArray, ddepth, dx, dy[, dst[, ksize[, scale[, delta[, borderType]]]]]) -> dst
.   @brief Calculates the first, second, third, or mixed image derivatives using an extended Sobel operator.
.   
.   In all cases except one, the \\f$\\texttt{ksize} \\times \\texttt{ksize}\\f$ separable kernel is used to
.   calculate the derivative. When \\f$\\texttt{ksize = 1}\\f$, the \\f$3 \\times 1\\f$ or \\f$1 \\times 3\\f$
.   kernel is used (that is, no Gaussian smoothing is done). `ksize = 1` can only be used for the first
.   or the second x- or y- derivatives.
.   
.   There is also the special value `ksize = #FILTER_SCHARR (-1)` that corresponds to the \\f$3\\times3\\f$ Scharr
.   filter that may give more accurate results than the \\f$3\\times3\\f$ Sobel. The Scharr aperture is
.   
.   \\f[\\vecthreethree{-3}{0}{3}{-10}{0}{10}{-3}{0}{3}\\f]
.   
.   for the x-derivative, or transposed for the y-derivative.
.   
.   The function calculates an image derivative by convolving the image with the appropriate kernel:
.   
.   \\f[\\texttt{dst} =  \\frac{\\partial^{xorder+yorder} \\texttt{src}}{\\partial x^{xorder} \\partial y^{yorder}}\\f]
.   
.   The Sobel operators combine Gaussian smoothing and differentiation, so the result is more or less
.   resistant to the noise. Most often, the function is called with ( xorder = 1, yorder = 0, ksize = 3)
.   or ( xorder = 0, yorder = 1, ksize = 3) to calculate the first x- or y- image derivative. The first
.   case corresponds to a kernel of:
.   
.   \\f[\\vecthreethree{-1}{0}{1}{-2}{0}{2}{-1}{0}{1}\\f]
.   
.   The second case corresponds to a kernel of:
.   
.   \\f[\\vecthreethree{-1}{-2}{-1}{0}{0}{0}{1}{2}{1}\\f]
.   
.   @param src input image.
.   @param dst output image of the same size and the same number of channels as src .
.   @param ddepth output image depth, see @ref filter_depths "combinations"; in the case of
.       8-bit input images it will result in truncated derivatives.
.   @param dx order of the derivative x.
.   @param dy order of the derivative y.
.   @param ksize size of the extended Sobel kernel; it must be 1, 3, 5, or 7.
.   @param scale optional scale factor for the computed derivative values; by default, no scaling is
.   applied (see #getDerivKernels for details).
.   @param delta optional delta value that is added to the results prior to storing them in dst.
.   @param borderType pixel extrapolation method, see #BorderTypes. #BORDER_WRAP is not supported.
.   @sa  Scharr, Laplacian, sepFilter2D, filter2D, GaussianBlur, cartToPolar'

    """
    # print('src',src,ddepth,dx,dy,ksize,scale,delta,borderType)
    _ = cv2.Sobel(src, ddepth, dx, dy, ksize, scale, delta, borderType)
    # print(_)
    return _


@rx_func()
def findHomography(srcPoints: NDArray,
                   dstPoints: NDArray,
                   method: create_enum("findHomography_method", ['0', 'RANSAC', 'LMEDS', 'RHO'], default='0'),
                   ransacReprojThreshold: int = 3,
                   mask: NDArray = None,
                   maxIters: int = 2000,
                   confidence: float = 0.995) -> NDArray:
    """    "findHomography(srcPoints, dstPoints[, method[, ransacReprojThreshold[, mask[, maxIters[, confidence]]]]]) -> retval, mask
.   @brief Finds a perspective transformation between two planes.
.   
.   @param srcPoints Coordinates of the points in the original plane, a matrix of the type CV_32FC2
.   or vector\\<Point2f\\> .
.   @param dstPoints Coordinates of the points in the target plane, a matrix of the type CV_32FC2 or
.   a vector\\<Point2f\\> .
.   @param method Method used to compute a homography matrix. The following methods are possible:
.   -   **0** - a regular method using all the points, i.e., the least squares method
.   -   **RANSAC** - RANSAC-based robust method
.   -   **LMEDS** - Least-Median robust method
.   -   **RHO** - PROSAC-based robust method
.   @param ransacReprojThreshold Maximum allowed reprojection error to treat a point pair as an inlier
.   (used in the RANSAC and RHO methods only). That is, if
.   \\f[\\| \\texttt{dstPoints} _i -  \\texttt{convertPointsHomogeneous} ( \\texttt{H} * \\texttt{srcPoints} _i) \\|_2  >  \\texttt{ransacReprojThreshold}\\f]
.   then the point \\f$i\\f$ is considered as an outlier. If srcPoints and dstPoints are measured in pixels,
.   it usually makes sense to set this parameter somewhere in the range of 1 to 10.
.   @param mask Optional output mask set by a robust method ( RANSAC or LMEDS ). Note that the input
.   mask values are ignored.
.   @param maxIters The maximum number of RANSAC iterations.
.   @param confidence Confidence level, between 0 and 1.
.   
.   The function finds and returns the perspective transformation \\f$H\\f$ between the source and the
.   destination planes:
.   
.   \\f[s_i  \\vecthree{x'_i}{y'_i}{1} \\sim H  \\vecthree{x_i}{y_i}{1}\\f]
.   
.   so that the back-projection error
.   
.   \\f[\\sum _i \\left ( x'_i- \\frac{h_{11} x_i + h_{12} y_i + h_{13}}{h_{31} x_i + h_{32} y_i + h_{33}} \\right )^2+ \\left ( y'_i- \\frac{h_{21} x_i + h_{22} y_i + h_{23}}{h_{31} x_i + h_{32} y_i + h_{33}} \\right )^2\\f]
.   
.   is minimized. If the parameter method is set to the default value 0, the function uses all the point
.   pairs to compute an initial homography estimate with a simple least-squares scheme.
.   
.   However, if not all of the point pairs ( \\f$srcPoints_i\\f$, \\f$dstPoints_i\\f$ ) fit the rigid perspective
.   transformation (that is, there are some outliers), this initial estimate will be poor. In this case,
.   you can use one of the three robust methods. The methods RANSAC, LMeDS and RHO try many different
.   random subsets of the corresponding point pairs (of four pairs each, collinear pairs are discarded), estimate the homography matrix
.   using this subset and a simple least-squares algorithm, and then compute the quality/goodness of the
.   computed homography (which is the number of inliers for RANSAC or the least median re-projection error for
.   LMeDS). The best subset is then used to produce the initial estimate of the homography matrix and
.   the mask of inliers/outliers.
.   
.   Regardless of the method, robust or not, the computed homography matrix is refined further (using
.   inliers only in case of a robust method) with the Levenberg-Marquardt method to reduce the
.   re-projection error even more.
.   
.   The methods RANSAC and RHO can handle practically any ratio of outliers but need a threshold to
.   distinguish inliers from outliers. The method LMeDS does not need any threshold but it works
.   correctly only when there are more than 50% of inliers. Finally, if there are no outliers and the
.   noise is rather small, use the default method (method=0).
.   
.   The function is used to find initial intrinsic and extrinsic matrices. Homography matrix is
.   determined up to a scale. Thus, it is normalized so that \\f$h_{33}=1\\f$. Note that whenever an \\f$H\\f$ matrix
.   cannot be estimated, an empty one will be returned.
.   
.   @sa
.   getAffineTransform, estimateAffine2D, estimateAffinePartial2D, getPerspectiveTransform, warpPerspective,
.   perspectiveTransform"

    """
    return cv2.findHomography(srcPoints, dstPoints, method, ransacReprojThreshold, mask, maxIters, confidence)


@rx_func()
def warpPerspective(src: NDArray,
                    M: NDArray,
                    dsize: int,
                    flags: ENUM_CV_InterpolationFlags = ENUM_CV_InterpolationFlags.INTER_LINEAR,
                    borderMode: ENUM_CV_BorderTypes = ENUM_CV_BorderTypes.BORDER_CONSTANT,
                    borderValue: tuple = (0, 0, 0)) -> NDArray:
    """    'warpPerspective(src:NDArray, M, dsize[, dst[, flags[, borderMode[, borderValue]]]]) -> dst
.   @brief Applies a perspective transformation to an image.
.   
.   The function warpPerspective transforms the source image using the specified matrix:
.   
.   \\f[\\texttt{dst} (x,y) =  \\texttt{src} \\left ( \\frac{M_{11} x + M_{12} y + M_{13}}{M_{31} x + M_{32} y + M_{33}} ,
.        \\frac{M_{21} x + M_{22} y + M_{23}}{M_{31} x + M_{32} y + M_{33}} \\right )\\f]
.   
.   when the flag #WARP_INVERSE_MAP is set. Otherwise, the transformation is first inverted with invert
.   and then put in the formula above instead of M. The function cannot operate in-place.
.   
.   @param src input image.
.   @param dst output image that has the size dsize and the same type as src .
.   @param M \\f$3\\times 3\\f$ transformation matrix.
.   @param dsize size of the output image.
.   @param flags combination of interpolation methods (#INTER_LINEAR or #INTER_NEAREST) and the
.   optional flag #WARP_INVERSE_MAP, that sets M as the inverse transformation (
.   \\f$\\texttt{dst}\\rightarrow\\texttt{src}\\f$ ).
.   @param borderMode pixel extrapolation method (#BORDER_CONSTANT or #BORDER_REPLICATE).
.   @param borderValue value used in case of a constant border; by default, it equals 0.
.   
.   @sa  warpAffine, resize, remap, getRectSubPix, perspectiveTransform'

    """
    cv2.warpPerspective(src, M, dsize, flags, borderMode, borderValue)


@rx_func()
def convexHull(points: NDArray,
               clockwise: bool = False,
               returnPoints: bool = True) -> NDArray:
    """    'convexHull(points[, hull[, clockwise[, returnPoints]]]) -> hull
.   @brief Finds the convex hull of a point set.
.   
.   The function cv::convexHull finds the convex hull of a 2D point set using the Sklansky\'s algorithm @cite Sklansky82
.   that has *O(N logN)* complexity in the current implementation.
.   
.   @param points Input 2D point set, stored in std::vector or Mat.
.   @param hull Output convex hull. It is either an integer vector of indices or vector of points. In
.   the first case, the hull elements are 0-based indices of the convex hull points in the original
.   array (since the set of convex hull points is a subset of the original point set). In the second
.   case, hull elements are the convex hull points themselves.
.   @param clockwise Orientation flag. If it is true, the output convex hull is oriented clockwise.
.   Otherwise, it is oriented counter-clockwise. The assumed coordinate system has its X axis pointing
.   to the right, and its Y axis pointing upwards.
.   @param returnPoints Operation flag. In case of a matrix, when the flag is true, the function
.   returns convex hull points. Otherwise, it returns indices of the convex hull points. When the
.   output array is std::vector, the flag is ignored, and the output depends on the type of the
.   vector: std::vecto<int> implies returnPoints=false, std::vector\\<Point\\> implies
.   returnPoints=true.
.   
.   @note `points` and `hull` should be different arrays, inplace processing isn\'t supported.
.   
.   Check @ref tutorial_hull "the corresponding tutorial" for more details.
.   
.   useful links:
.   
.   https://www.learnopencv.com/convex-hull-using-opencv-in-python-and-c/'

    """
    return cv2.convexHull(points, clockwise, returnPoints)


@rx_func()
def findContours(image: NDArray,
                 mode: ENUM_CV_RetrievalModes,
                 method: ENUM_CV_ContourApproximationModes,
                 offset: tuple = (0, 0)) -> np.ndarray:
    """    "findContours(image, mode, method[, contours[, hierarchy[, offset]]]) -> contours, hierarchy
.   @brief Finds contours in a binary image.
.   
.   The function retrieves contours from the binary image using the algorithm @cite Suzuki85 . The contours
.   are a useful tool for shape analysis and object detection and recognition. See squares.cpp in the
.   OpenCV sample directory.
.   @note Since opencv 3.2 source image is not modified by this function.
.   
.   @param image Source, an 8-bit single-channel image. Non-zero pixels are treated as 1's. Zero
.   pixels remain 0's, so the image is treated as binary . You can use #compare, #inRange, #threshold ,
.   #adaptiveThreshold, #Canny, and others to create a binary image out of a grayscale or color one.
.   If mode equals to #RETR_CCOMP or #RETR_FLOODFILL, the input can also be a 32-bit integer image of labels (CV_32SC1).
.   @param contours Detected contours. Each contour is stored as a vector of points (e.g.
.   std::vector<std::vector<cv::Point> >).
.   @param hierarchy Optional output vector (e.g. std::vector<cv::Vec4i>), containing information about the image topology. It has
.   as many elements as the number of contours. For each i-th contour contours[i], the elements
.   hierarchy[i][0] , hierarchy[i][1] , hierarchy[i][2] , and hierarchy[i][3] are set to 0-based indices
.   in contours of the next and previous contours at the same hierarchical level, the first child
.   contour and the parent contour, respectively. If for the contour i there are no next, previous,
.   parent, or nested contours, the corresponding elements of hierarchy[i] will be negative.
.   @param mode Contour retrieval mode, see #RetrievalModes
.   @param method Contour approximation method, see #ContourApproximationModes
.   @param offset Optional offset by which every contour point is shifted. This is useful if the
.   contours are extracted from the image ROI and then they should be analyzed in the whole image
.   context."

    """
    return cv2.findContours(image, mode, method=method, offset=offset)[0]


@rx_func()
def findContours_origin(image: NDArray,
                        mode: ENUM_CV_RetrievalModes,
                        method: ENUM_CV_ContourApproximationModes,
                        offset: tuple = (0, 0)) -> Tuple:
    """    "findContours(image, mode, method[, contours[, hierarchy[, offset]]]) -> contours, hierarchy
.   @brief Finds contours in a binary image.
.   
.   The function retrieves contours from the binary image using the algorithm @cite Suzuki85 . The contours
.   are a useful tool for shape analysis and object detection and recognition. See squares.cpp in the
.   OpenCV sample directory.
.   @note Since opencv 3.2 source image is not modified by this function.
.   
.   @param image Source, an 8-bit single-channel image. Non-zero pixels are treated as 1's. Zero
.   pixels remain 0's, so the image is treated as binary . You can use #compare, #inRange, #threshold ,
.   #adaptiveThreshold, #Canny, and others to create a binary image out of a grayscale or color one.
.   If mode equals to #RETR_CCOMP or #RETR_FLOODFILL, the input can also be a 32-bit integer image of labels (CV_32SC1).
.   @param contours Detected contours. Each contour is stored as a vector of points (e.g.
.   std::vector<std::vector<cv::Point> >).
.   @param hierarchy Optional output vector (e.g. std::vector<cv::Vec4i>), containing information about the image topology. It has
.   as many elements as the number of contours. For each i-th contour contours[i], the elements
.   hierarchy[i][0] , hierarchy[i][1] , hierarchy[i][2] , and hierarchy[i][3] are set to 0-based indices
.   in contours of the next and previous contours at the same hierarchical level, the first child
.   contour and the parent contour, respectively. If for the contour i there are no next, previous,
.   parent, or nested contours, the corresponding elements of hierarchy[i] will be negative.
.   @param mode Contour retrieval mode, see #RetrievalModes
.   @param method Contour approximation method, see #ContourApproximationModes
.   @param offset Optional offset by which every contour point is shifted. This is useful if the
.   contours are extracted from the image ROI and then they should be analyzed in the whole image
.   context."

    """
    return cv2.findContours(image, mode, method=method, offset=offset)


@rx_func()
def moments(array: NDArray, binaryImage: bool = False) -> NDArray:
    """    "moments(array[, binaryImage]) -> retval
.   @brief Calculates all of the moments up to the third order of a polygon or rasterized shape.
.   
.   The function computes moments, up to the 3rd order, of a vector shape or a rasterized shape. The
.   results are returned in the structure cv::Moments.
.   
.   @param array Raster image (single-channel, 8-bit or floating-point 2D array) or an array (
.   \\f$1 \\times N\\f$ or \\f$N \\times 1\\f$ ) of 2D points (Point or Point2f ).
.   @param binaryImage If it is true, all non-zero image pixels are treated as 1's. The parameter is
.   used for images only.
.   @returns moments.
.   
.   @note Only applicable to contour moments calculations from Python bindings: Note that the numpy
.   type for the input array should be either np.int32 or np.float32.
.   
.   @sa  contourArea, arcLength"

    """
    return cv2.moments(array, binaryImage)


@rx_func()
def inRange(src: NDArray, lowerb: NDArray, upperb: NDArray) -> NDArray:
    """    'inRange(src:NDArray, lowerb, upperb[, dst]) -> dst
.   @brief  Checks if array elements lie between the elements of two other arrays.
.   
.   The function checks the range as follows:
.   -   For every element of a single-channel input array:
.       \\f[\\texttt{dst} (I)= \\texttt{lowerb} (I)_0  \\leq \\texttt{src} (I)_0 \\leq  \\texttt{upperb} (I)_0\\f]
.   -   For two-channel arrays:
.       \\f[\\texttt{dst} (I)= \\texttt{lowerb} (I)_0  \\leq \\texttt{src} (I)_0 \\leq  \\texttt{upperb} (I)_0  \\land \\texttt{lowerb} (I)_1  \\leq \\texttt{src} (I)_1 \\leq  \\texttt{upperb} (I)_1\\f]
.   -   and so forth.
.   
.   That is, dst (I) is set to 255 (all 1 -bits) if src (I) is within the
.   specified 1D, 2D, 3D, ... box and 0 otherwise.
.   
.   When the lower and/or upper boundary parameters are scalars, the indexes
.   (I) at lowerb and upperb in the above formulas should be omitted.
.   @param src first input array.
.   @param lowerb inclusive lower boundary array or a scalar.
.   @param upperb inclusive upper boundary array or a scalar.
.   @param dst output array of the same size as src and CV_8U type.'

    """
    return cv2.inRange(src, lowerb, upperb)


@rx_func()
def bitwise_and(src1: NDArray, src2: NDArray,  mask: NDArray = None) -> NDArray:
    """    'bitwise_and(src1, src2[, dst[, mask]]) -> dst
.   @brief computes bitwise conjunction of the two arrays (dst = src1 & src2)
.   Calculates the per-element bit-wise conjunction of two arrays or an
.   array and a scalar.
.   
.   The function cv::bitwise_and calculates the per-element bit-wise logical conjunction for:
.   *   Two arrays when src1 and src2 have the same size:
.       \\f[\\texttt{dst} (I) =  \\texttt{src1} (I)  \\wedge \\texttt{src2} (I) \\quad \\texttt{if mask} (I) \
e0\\f]
.   *   An array and a scalar when src2 is constructed from Scalar or has
.       the same number of elements as `src1.channels()`:
.       \\f[\\texttt{dst} (I) =  \\texttt{src1} (I)  \\wedge \\texttt{src2} \\quad \\texttt{if mask} (I) \
e0\\f]
.   *   A scalar and an array when src1 is constructed from Scalar or has
.       the same number of elements as `src2.channels()`:
.       \\f[\\texttt{dst} (I) =  \\texttt{src1}  \\wedge \\texttt{src2} (I) \\quad \\texttt{if mask} (I) \
e0\\f]
.   In case of floating-point arrays, their machine-specific bit
.   representations (usually IEEE754-compliant) are used for the operation.
.   In case of multi-channel arrays, each channel is processed
.   independently. In the second and third cases above, the scalar is first
.   converted to the array type.
.   @param src1 first input array or a scalar.
.   @param src2 second input array or a scalar.
.   @param dst output array that has the same size and type as the input
.   arrays.
.   @param mask optional operation mask, 8-bit single channel array, that
.   specifies elements of the output array to be changed.'

    """
    return cv2.bitwise_and(src1, src2, mask)


@rx_func()
def bitwise_and(src1: NDArray, src2: NDArray,  mask: NDArray = None) -> NDArray:
    return cv2.bitwise_not(src1, src2, mask)


@rx_func()
def bitwise_not(src: NDArray,   mask: NDArray = None) -> NDArray:
    """    'bitwise_not(src[, dst[, mask]]) -> dst
.   @brief  Inverts every bit of an array.
.   
.   The function cv::bitwise_not calculates per-element bit-wise inversion of the input
.   array:
.   \\f[\\texttt{dst} (I) =  \
eg \\texttt{src} (I)\\f]
.   In case of a floating-point input array, its machine-specific bit
.   representation (usually IEEE754-compliant) is used for the operation. In
.   case of multi-channel arrays, each channel is processed independently.
.   @param src input array.
.   @param dst output array that has the same size and type as the input
.   array.
.   @param mask optional operation mask, 8-bit single channel array, that
.   specifies elements of the output array to be changed.'

    """
    return cv2.bitwise_not(src, mask)


@rx_func()
def getAffineTransform(src: NDArray) -> NDArray:
    """    'getAffineTransform(src:NDArray, dst) -> retval
.   @overload'

    """
    return cv2.getAffineTransform(src)


@rx_func()
def seamlessClone(src: NDArray, dst: NDArray, mask: NDArray, p: tuple, flags: ENUM_CV_InterpolationFlags = ENUM_CV_InterpolationFlags.INTER_LINEAR,) -> NDArray:
    """    'seamlessClone(src:NDArray, dst, mask, p, flags[, blend]) -> blend
.   @brief Image editing tasks concern either global changes (color/intensity corrections, filters,
.   deformations) or local changes concerned to a selection. Here we are interested in achieving local
.   changes, ones that are restricted to a region manually selected (ROI), in a seamless and effortless
.   manner. The extent of the changes ranges from slight distortions to complete replacement by novel
.   content @cite PM03 .
.   
.   @param src Input 8-bit 3-channel image.
.   @param dst Input 8-bit 3-channel image.
.   @param mask Input 8-bit 1 or 3-channel image.
.   @param p Point in dst image where object is placed.
.   @param blend Output image with the same size and type as dst.
.   @param flags Cloning method that could be cv::NORMAL_CLONE, cv::MIXED_CLONE or cv::MONOCHROME_TRANSFER'

    """
    # print(src.shape, dst.shape, mask.shape)
    return cv2.seamlessClone(src, dst, mask, p, flags,)


@rx_func()
def add(src1: NDArray, src2: NDArray,  mask: NDArray = None, dtype: int = -1) -> NDArray:
    """    'add(src1, src2[, dst[, mask[, dtype]]]) -> dst
.   @brief Calculates the per-element sum of two arrays or an array and a scalar.
.   
.   The function add calculates:
.   - Sum of two arrays when both input arrays have the same size and the same number of channels:
.   \\f[\\texttt{dst}(I) =  \\texttt{saturate} ( \\texttt{src1}(I) +  \\texttt{src2}(I)) \\quad \\texttt{if mask}(I) \
e0\\f]
.   - Sum of an array and a scalar when src2 is constructed from Scalar or has the same number of
.   elements as `src1.channels()`:
.   \\f[\\texttt{dst}(I) =  \\texttt{saturate} ( \\texttt{src1}(I) +  \\texttt{src2} ) \\quad \\texttt{if mask}(I) \
e0\\f]
.   - Sum of a scalar and an array when src1 is constructed from Scalar or has the same number of
.   elements as `src2.channels()`:
.   \\f[\\texttt{dst}(I) =  \\texttt{saturate} ( \\texttt{src1} +  \\texttt{src2}(I) ) \\quad \\texttt{if mask}(I) \
e0\\f]
.   where `I` is a multi-dimensional index of array elements. In case of multi-channel arrays, each
.   channel is processed independently.
.   
.   The first function in the list above can be replaced with matrix expressions:
.   @code{.cpp}
.       dst = src1 + src2;
.       dst += src1; // equivalent to add(dst, src1, dst);
.   @endcode
.   The input arrays and the output array can all have the same or different depths. For example, you
.   can add a 16-bit unsigned array to a 8-bit signed array and store the sum as a 32-bit
.   floating-point array. Depth of the output array is determined by the dtype parameter. In the second
.   and third cases above, as well as in the first case, when src1.depth() == src2.depth(), dtype can
.   be set to the default -1. In this case, the output array will have the same depth as the input
.   array, be it src1, src2 or both.
.   @note Saturation is not applied when the output array has the depth CV_32S. You may even get
.   result of an incorrect sign in the case of overflow.
.   @param src1 first input array or a scalar.
.   @param src2 second input array or a scalar.
.   @param dst output array that has the same size and number of channels as the input array(s); the
.   depth is defined by dtype or src1/src2.
.   @param mask optional operation mask - 8-bit single channel array, that specifies elements of the
.   output array to be changed.
.   @param dtype optional depth of the output array (see the discussion below).
.   @sa subtract, addWeighted, scaleAdd, Mat::convertTo'

    """
    return cv2.add(src1, src2, mask, dtype)


@rx_func()
def addWeighted(src1: NDArray, alpha: float, src2: NDArray, beta: float, gamma: float,  dtype: int = -1) -> NDArray:
    """    'addWeighted(src1, alpha, src2, beta, gamma[, dst[, dtype]]) -> dst
.   @brief Calculates the weighted sum of two arrays.
.   
.   The function addWeighted calculates the weighted sum of two arrays as follows:
.   \\f[\\texttt{dst} (I)= \\texttt{saturate} ( \\texttt{src1} (I)* \\texttt{alpha} +  \\texttt{src2} (I)* \\texttt{beta} +  \\texttt{gamma} )\\f]
.   where I is a multi-dimensional index of array elements. In case of multi-channel arrays, each
.   channel is processed independently.
.   The function can be replaced with a matrix expression:
.   @code{.cpp}
.       dst = src1*alpha + src2*beta + gamma;
.   @endcode
.   @note Saturation is not applied when the output array has the depth CV_32S. You may even get
.   result of an incorrect sign in the case of overflow.
.   @param src1 first input array.
.   @param alpha weight of the first array elements.
.   @param src2 second input array of the same size and channel number as src1.
.   @param beta weight of the second array elements.
.   @param gamma scalar added to each sum.
.   @param dst output array that has the same size and number of channels as the input arrays.
.   @param dtype optional depth of the output array; when both input arrays have the same depth, dtype
.   can be set to -1, which will be equivalent to src1.depth().
.   @sa  add, subtract, scaleAdd, Mat::convertTo'

    """
    return cv2.addWeighted(src1, alpha, src2, beta, gamma, dtype)


@rx_func()
def matchShapes(contour1: NDArray, contour2: NDArray, method: ENUM_CV_ShapeMatchModes, parameter: float) -> NDArray:
    """    'matchShapes(contour1, contour2, method, parameter) -> retval
.   @brief Compares two shapes.
.   
.   The function compares two shapes. All three implemented methods use the Hu invariants (see #HuMoments)
.   
.   @param contour1 First contour or grayscale image.
.   @param contour2 Second contour or grayscale image.
.   @param method Comparison method, see #ShapeMatchModes
.   @param parameter Method-specific parameter (not supported now).'

    """
    return cv2.matchShapes(contour1, contour2, method, parameter)


@rx_func()
def pyrDown(src: NDArray,  dstsize: tuple = None, borderType: ENUM_CV_BorderTypes = ENUM_CV_BorderTypes.default) -> NDArray:
    """    "pyrDown(src[, dst[, dstsize[, borderType]]]) -> dst
.   @brief Blurs an image and downsamples it.
.   
.   By default, size of the output image is computed as `Size((src.cols+1)/2, (src.rows+1)/2)`, but in
.   any case, the following conditions should be satisfied:
.   
.   \\f[\\begin{array}{l} | \\texttt{dstsize.width} *2-src.cols| \\leq 2 \\\\ | \\texttt{dstsize.height} *2-src.rows| \\leq 2 \\end{array}\\f]
.   
.   The function performs the downsampling step of the Gaussian pyramid construction. First, it
.   convolves the source image with the kernel:
.   
.   \\f[\\frac{1}{256} \\begin{bmatrix} 1 & 4 & 6 & 4 & 1  \\\\ 4 & 16 & 24 & 16 & 4  \\\\ 6 & 24 & 36 & 24 & 6  \\\\ 4 & 16 & 24 & 16 & 4  \\\\ 1 & 4 & 6 & 4 & 1 \\end{bmatrix}\\f]
.   
.   Then, it downsamples the image by rejecting even rows and columns.
.   
.   @param src input image.
.   @param dst output image; it has the specified size and the same type as src.
.   @param dstsize size of the output image.
.   @param borderType Pixel extrapolation method, see #BorderTypes (#BORDER_CONSTANT isn't supported)"

    """
    return cv2.pyrDown(src, dstsize, borderType)


@rx_func()
def blur(src: NDArray, ksize: tuple, anchor: tuple = (-1, -1), borderType: ENUM_CV_BorderTypes = ENUM_CV_BorderTypes.default) -> NDArray:
    """    'blur(src:NDArray, ksize[, dst[, anchor[, borderType]]]) -> dst
.   @brief Blurs an image using the normalized box filter.
.   
.   The function smooths an image using the kernel:
.   
.   \\f[\\texttt{K} =  \\frac{1}{\\texttt{ksize.width*ksize.height}} \\begin{bmatrix} 1 & 1 & 1 &  \\cdots & 1 & 1  \\\\ 1 & 1 & 1 &  \\cdots & 1 & 1  \\\\ \\hdotsfor{6} \\\\ 1 & 1 & 1 &  \\cdots & 1 & 1  \\\\ \\end{bmatrix}\\f]
.   
.   The call `blur(src:NDArray, dst, ksize, anchor, borderType)` is equivalent to `boxFilter(src:NDArray, dst, src.type(), ksize,
.   anchor, true, borderType)`.
.   
.   @param src input image; it can have any number of channels, which are processed independently, but
.   the depth should be CV_8U, CV_16U, CV_16S, CV_32F or CV_64F.
.   @param dst output image of the same size and type as src.
.   @param ksize blurring kernel size.
.   @param anchor anchor point; default value Point(-1,-1) means that the anchor is at the kernel
.   center.
.   @param borderType border mode used to extrapolate pixels outside of the image, see #BorderTypes. #BORDER_WRAP is not supported.
.   @sa  boxFilter, bilateralFilter, GaussianBlur, medianBlur'

    """
    return cv2.blur(src, ksize, anchor=anchor, borderType=borderType)


@rx_func()
def getRotationMatrix2D(center: tuple, angle: float, scale: float) -> NDArray:
    """    'getRotationMatrix2D(center, angle, scale) -> retval
.   @brief Calculates an affine matrix of 2D rotation.
.   
.   The function calculates the following matrix:
.   
.   \\f[\\begin{bmatrix} \\alpha &  \\beta & (1- \\alpha )  \\cdot \\texttt{center.x} -  \\beta \\cdot \\texttt{center.y} \\\\ - \\beta &  \\alpha &  \\beta \\cdot \\texttt{center.x} + (1- \\alpha )  \\cdot \\texttt{center.y} \\end{bmatrix}\\f]
.   
.   where
.   
.   \\f[\\begin{array}{l} \\alpha =  \\texttt{scale} \\cdot \\cos \\texttt{angle} , \\\\ \\beta =  \\texttt{scale} \\cdot \\sin \\texttt{angle} \\end{array}\\f]
.   
.   The transformation maps the rotation center to itself. If this is not the target, adjust the shift.
.   
.   @param center Center of the rotation in the source image.
.   @param angle Rotation angle in degrees. Positive values mean counter-clockwise rotation (the
.   coordinate origin is assumed to be the top-left corner).
.   @param scale Isotropic scale factor.
.   
.   @sa  getAffineTransform, warpAffine, transform'

    """
    return cv2.getRotationMatrix2D(center, angle, scale)


@rx_func()
def merge(mv: NDArray) -> NDArray:
    """    'merge(mv[, dst]) -> dst
.   @overload
.   @param mv input vector of matrices to be merged; all the matrices in mv must have the same
.   size and the same depth.
.   @param dst output array of the same size and the same depth as mv[0]; The number of channels will
.   be the total number of channels in the matrix array.'

    """
    return cv2.merge(mv)


@rx_func()
def multiply(src1: NDArray, src2: NDArray, scale: float = 1.0, dtype: int = -1) -> NDArray:
    """    'multiply(src1, src2[, dst[, scale[, dtype]]]) -> dst
.   @brief Calculates the per-element scaled product of two arrays.
.   
.   The function multiply calculates the per-element product of two arrays:
.   
.   \\f[\\texttt{dst} (I)= \\texttt{saturate} ( \\texttt{scale} \\cdot \\texttt{src1} (I)  \\cdot \\texttt{src2} (I))\\f]
.   
.   There is also a @ref MatrixExpressions -friendly variant of the first function. See Mat::mul .
.   
.   For a not-per-element matrix product, see gemm .
.   
.   @note Saturation is not applied when the output array has the depth
.   CV_32S. You may even get result of an incorrect sign in the case of
.   overflow.
.   @param src1 first input array.
.   @param src2 second input array of the same size and the same type as src1.
.   @param dst output array of the same size and type as src1.
.   @param scale optional scale factor.
.   @param dtype optional depth of the output array
.   @sa add, subtract, divide, scaleAdd, addWeighted, accumulate, accumulateProduct, accumulateSquare,
.   Mat::convertTo'

    """
    return cv2.multiply(src1, src2, scale, dtype)


@rx_func()
def drawContours(image: NDArray,
                 contours: NDArray,
                 contourIdx: int,
                 color: tuple = (255, 255, 255),
                 thickness: int = 1,
                 lineType: int = 1,
                 hierarchy: NDArray = None,
                 maxLevel: create_enum("drawContours_maxLevel", [
                                       0, 1, 2], default=0) = None,
                 offset: tuple = (0, 0)) -> NDArray:
    """    'drawContours(image, contours, contourIdx, color[, thickness[, lineType[, hierarchy[, maxLevel[, offset]]]]]) -> image
.   @brief Draws contours outlines or filled contours.
.   
.   The function draws contour outlines in the image if \\f$\\texttt{thickness} \\ge 0\\f$ or fills the area
.   bounded by the contours if \\f$\\texttt{thickness}<0\\f$ . The example below shows how to retrieve
.   connected components from the binary image and label them: :
.   @include snippets/imgproc_drawContours.cpp
.   
.   @param image Destination image.
.   @param contours All the input contours. Each contour is stored as a point vector.
.   @param contourIdx Parameter indicating a contour to draw. If it is negative, all the contours are drawn.
.   @param color Color of the contours.
.   @param thickness Thickness of lines the contours are drawn with. If it is negative (for example,
.   thickness=#FILLED ), the contour interiors are drawn.
.   @param lineType Line connectivity. See #LineTypes
.   @param hierarchy Optional information about hierarchy. It is only needed if you want to draw only
.   some of the contours (see maxLevel ).
.   @param maxLevel Maximal level for drawn contours. If it is 0, only the specified contour is drawn.
.   If it is 1, the function draws the contour(s) and all the nested contours. If it is 2, the function
.   draws the contours, all the nested contours, all the nested-to-nested contours, and so on. This
.   parameter is only taken into account when there is hierarchy available.
.   @param offset Optional contour shift parameter. Shift all the drawn contours by the specified
.   \\f$\\texttt{offset}=(dx,dy)\\f$ .
.   @note When thickness=#FILLED, the function is designed to handle connected components with holes correctly
.   even when no hierarchy date is provided. This is done by analyzing all the outlines together
.   using even-odd rule. This may give incorrect results if you have a joint collection of separately retrieved
.   contours. In order to solve this problem, you need to call #drawContours separately for each sub-group
.   of contours, or iterate over the collection using contourIdx parameter.'

    """
    cv2.drawContours(image, contours, contourIdx, color,
                     thickness, lineType, hierarchy, maxLevel, offset)


@rx_func()
def flip(src: NDArray, flipCode: create_enum("flip_flipCode", [-1, 0, 1], default=0)) -> NDArray:
    """    'flip(src:NDArray, flipCode[, dst]) -> dst
.   @brief Flips a 2D array around vertical, horizontal, or both axes.
.   
.   The function cv::flip flips the array in one of three different ways (row
.   and column indices are 0-based):
.   \\f[\\texttt{dst} _{ij} =
.   \\left\\{
.   \\begin{array}{l l}
.   \\texttt{src} _{\\texttt{src.rows}-i-1,j} & if\\;  \\texttt{flipCode} = 0 \\\\
.   \\texttt{src} _{i, \\texttt{src.cols} -j-1} & if\\;  \\texttt{flipCode} > 0 \\\\
.   \\texttt{src} _{ \\texttt{src.rows} -i-1, \\texttt{src.cols} -j-1} & if\\; \\texttt{flipCode} < 0 \\\\
.   \\end{array}
.   \\right.\\f]
.   The example scenarios of using the function are the following:
.   *   Vertical flipping of the image (flipCode == 0) to switch between
.       top-left and bottom-left image origin. This is a typical operation
.       in video processing on Microsoft Windows\\* OS.
.   *   Horizontal flipping of the image with the subsequent horizontal
.       shift and absolute difference calculation to check for a
.       vertical-axis symmetry (flipCode \\> 0).
.   *   Simultaneous horizontal and vertical flipping of the image with
.       the subsequent shift and absolute difference calculation to check
.       for a central symmetry (flipCode \\< 0).
.   *   Reversing the order of point arrays (flipCode \\> 0 or
.       flipCode == 0).
.   @param src input array.
.   @param dst output array of the same size and type as src.
.   @param flipCode a flag to specify how to flip the array; 0 means
.   flipping around the x-axis and positive value (for example, 1) means
.   flipping around y-axis. Negative value (for example, -1) means flipping
.   around both axes.
.   @sa transpose , repeat , completeSymm'

    """
    return cv2.flip(src, flipCode)


@rx_func()
def floodFill(image: NDArray, mask: NDArray, seedPoint: tuple, newVal: tuple, loDiff: tuple = (0, 0, 0), upDiff: tuple = (0, 0, 0),
              flags: ENUM_CV_FloodFillFlags = ENUM_CV_FloodFillFlags.default) -> NDArray:
    """    "floodFill(image, mask, seedPoint, newVal[, loDiff[, upDiff[, flags]]]) -> retval, image, mask, rect
.   @brief Fills a connected component with the given color.
.   
.   The function cv::floodFill fills a connected component starting from the seed point with the specified
.   color. The connectivity is determined by the color/brightness closeness of the neighbor pixels. The
.   pixel at \\f$(x,y)\\f$ is considered to belong to the repainted domain if:
.   
.   - in case of a grayscale image and floating range
.   \\f[\\texttt{src} (x',y')- \\texttt{loDiff} \\leq \\texttt{src} (x,y)  \\leq \\texttt{src} (x',y')+ \\texttt{upDiff}\\f]
.   
.   
.   - in case of a grayscale image and fixed range
.   \\f[\\texttt{src} ( \\texttt{seedPoint} .x, \\texttt{seedPoint} .y)- \\texttt{loDiff} \\leq \\texttt{src} (x,y)  \\leq \\texttt{src} ( \\texttt{seedPoint} .x, \\texttt{seedPoint} .y)+ \\texttt{upDiff}\\f]
.   
.   
.   - in case of a color image and floating range
.   \\f[\\texttt{src} (x',y')_r- \\texttt{loDiff} _r \\leq \\texttt{src} (x,y)_r \\leq \\texttt{src} (x',y')_r+ \\texttt{upDiff} _r,\\f]
.   \\f[\\texttt{src} (x',y')_g- \\texttt{loDiff} _g \\leq \\texttt{src} (x,y)_g \\leq \\texttt{src} (x',y')_g+ \\texttt{upDiff} _g\\f]
.   and
.   \\f[\\texttt{src} (x',y')_b- \\texttt{loDiff} _b \\leq \\texttt{src} (x,y)_b \\leq \\texttt{src} (x',y')_b+ \\texttt{upDiff} _b\\f]
.   
.   
.   - in case of a color image and fixed range
.   \\f[\\texttt{src} ( \\texttt{seedPoint} .x, \\texttt{seedPoint} .y)_r- \\texttt{loDiff} _r \\leq \\texttt{src} (x,y)_r \\leq \\texttt{src} ( \\texttt{seedPoint} .x, \\texttt{seedPoint} .y)_r+ \\texttt{upDiff} _r,\\f]
.   \\f[\\texttt{src} ( \\texttt{seedPoint} .x, \\texttt{seedPoint} .y)_g- \\texttt{loDiff} _g \\leq \\texttt{src} (x,y)_g \\leq \\texttt{src} ( \\texttt{seedPoint} .x, \\texttt{seedPoint} .y)_g+ \\texttt{upDiff} _g\\f]
.   and
.   \\f[\\texttt{src} ( \\texttt{seedPoint} .x, \\texttt{seedPoint} .y)_b- \\texttt{loDiff} _b \\leq \\texttt{src} (x,y)_b \\leq \\texttt{src} ( \\texttt{seedPoint} .x, \\texttt{seedPoint} .y)_b+ \\texttt{upDiff} _b\\f]
.   
.   
.   where \\f$src(x',y')\\f$ is the value of one of pixel neighbors that is already known to belong to the
.   component. That is, to be added to the connected component, a color/brightness of the pixel should
.   be close enough to:
.   - Color/brightness of one of its neighbors that already belong to the connected component in case
.   of a floating range.
.   - Color/brightness of the seed point in case of a fixed range.
.   
.   Use these functions to either mark a connected component with the specified color in-place, or build
.   a mask and then extract the contour, or copy the region to another image, and so on.
.   
.   @param image Input/output 1- or 3-channel, 8-bit, or floating-point image. It is modified by the
.   function unless the #FLOODFILL_MASK_ONLY flag is set in the second variant of the function. See
.   the details below.
.   @param mask Operation mask that should be a single-channel 8-bit image, 2 pixels wider and 2 pixels
.   taller than image. Since this is both an input and output parameter, you must take responsibility
.   of initializing it. Flood-filling cannot go across non-zero pixels in the input mask. For example,
.   an edge detector output can be used as a mask to stop filling at edges. On output, pixels in the
.   mask corresponding to filled pixels in the image are set to 1 or to the a value specified in flags
.   as described below. Additionally, the function fills the border of the mask with ones to simplify
.   internal processing. It is therefore possible to use the same mask in multiple calls to the function
.   to make sure the filled areas do not overlap.
.   @param seedPoint Starting point.
.   @param newVal New value of the repainted domain pixels.
.   @param loDiff Maximal lower brightness/color difference between the currently observed pixel and
.   one of its neighbors belonging to the component, or a seed pixel being added to the component.
.   @param upDiff Maximal upper brightness/color difference between the currently observed pixel and
.   one of its neighbors belonging to the component, or a seed pixel being added to the component.
.   @param rect Optional output parameter set by the function to the minimum bounding rectangle of the
.   repainted domain.
.   @param flags Operation flags. The first 8 bits contain a connectivity value. The default value of
.   4 means that only the four nearest neighbor pixels (those that share an edge) are considered. A
.   connectivity value of 8 means that the eight nearest neighbor pixels (those that share a corner)
.   will be considered. The next 8 bits (8-16) contain a value between 1 and 255 with which to fill
.   the mask (the default value is 1). For example, 4 | ( 255 \\<\\< 8 ) will consider 4 nearest
.   neighbours and fill the mask with a value of 255. The following additional options occupy higher
.   bits and therefore may be further combined with the connectivity and mask fill values using
.   bit-wise or (|), see #FloodFillFlags.
.   
.   @note Since the mask is larger than the filled image, a pixel \\f$(x, y)\\f$ in image corresponds to the
.   pixel \\f$(x+1, y+1)\\f$ in the mask .
.   
.   @sa findContours"

    """
    return cv2.floodFill(image, mask, seedPoint, newVal, loDiff, upDiff, flags)


@rx_func()
def edgePreservingFilter(src: NDArray,
                         flags: ENUM_CV_InterpolationFlags = ENUM_CV_InterpolationFlags.INTER_LINEAR, sigma_s: int = 60, sigma_r: float = 0.4) -> NDArray:
    """    'edgePreservingFilter(src[, dst[, flags[, sigma_s[, sigma_r]]]]) -> dst
.   @brief Filtering is the fundamental operation in image and video processing. Edge-preserving smoothing
.   filters are used in many different applications @cite EM11 .
.   
.   @param src Input 8-bit 3-channel image.
.   @param dst Output 8-bit 3-channel image.
.   @param flags Edge preserving filters: cv::RECURS_FILTER or cv::NORMCONV_FILTER
.   @param sigma_s %Range between 0 to 200.
.   @param sigma_r %Range between 0 to 1.'

    """
    return cv2.edgePreservingFilter(src, flags=flags, sigma_s=sigma_s, sigma_r=sigma_r)


@rx_func()
def fillPoly(img: NDArray, pts: NDArray, color: tuple = (255, 255, 255), lineType: int = 1, shift: int = 0, offset: tuple = None) -> NDArray:
    """    'fillPoly(img:NDArray, pts, color[, lineType[, shift[, offset]]]) -> img
.   @brief Fills the area bounded by one or more polygons.
.   
.   The function cv::fillPoly fills an area bounded by several polygonal contours. The function can fill
.   complex areas, for example, areas with holes, contours with self-intersections (some of their
.   parts), and so forth.
.   
.   @param img Image.
.   @param pts Array of polygons where each polygon is represented as an array of points.
.   @param color Polygon color.
.   @param lineType Type of the polygon boundaries. See #LineTypes
.   @param shift Number of fractional bits in the vertex coordinates.
.   @param offset Optional offset of all points of the contours.'

    """
    return cv2.fillPoly(img, pts, color, lineType, shift, offset)


@rx_func()
def subtract(src1: NDArray, src2: NDArray, mask: NDArray = None, dtype: int = -1) -> NDArray:
    """    'subtract(src1, src2[, dst[, mask[, dtype]]]) -> dst
.   @brief Calculates the per-element difference between two arrays or array and a scalar.
.   
.   The function subtract calculates:
.   - Difference between two arrays, when both input arrays have the same size and the same number of
.   channels:
.       \\f[\\  {dst}(I) =  \\texttt{saturate} ( \\texttt{src1}(I) -  \\texttt{src2}(I)) \\quad \\texttt{if mask}(I) \
e0\\f]
.   - Difference between an array and a scalar, when src2 is constructed from Scalar or has the same
.   number of elements as `src1.channels()`:
.       \\f[\\texttt{dst}(I) =  \\texttt{saturate} ( \\texttt{src1}(I) -  \\texttt{src2} ) \\quad \\texttt{if mask}(I) \
e0\\f]
.   - Difference between a scalar and an array, when src1 is constructed from Scalar or has the same
.   number of elements as `src2.channels()`:
.       \\f[\\texttt{dst}(I) =  \\texttt{saturate} ( \\texttt{src1} -  \\texttt{src2}(I) ) \\quad \\texttt{if mask}(I) \
e0\\f]
.   - The reverse difference between a scalar and an array in the case of `SubRS`:
.       \\f[\\texttt{dst}(I) =  \\texttt{saturate} ( \\texttt{src2} -  \\texttt{src1}(I) ) \\quad \\texttt{if mask}(I) \
e0\\f]
.   where I is a multi-dimensional index of array elements. In case of multi-channel arrays, each
.   channel is processed independently.
.   
.   The first function in the list above can be replaced with matrix expressions:
.   @code{.cpp}
.       dst = src1 - src2;
.       dst -= src1; // equivalent to subtract(dst, src1, dst);
.   @endcode
.   The input arrays and the output array can all have the same or different depths. For example, you
.   can subtract to 8-bit unsigned arrays and store the difference in a 16-bit signed array. Depth of
.   the output array is determined by dtype parameter. In the second and third cases above, as well as
.   in the first case, when src1.depth() == src2.depth(), dtype can be set to the default -1. In this
.   case the output array will have the same depth as the input array, be it src1, src2 or both.
.   @note Saturation is not applied when the output array has the depth CV_32S. You may even get
.   result of an incorrect sign in the case of overflow.
.   @param src1 first input array or a scalar.
.   @param src2 second input array or a scalar.
.   @param dst output array of the same size and the same number of channels as the input array.
.   @param mask optional operation mask; this is an 8-bit single channel array that specifies elements
.   of the output array to be changed.
.   @param dtype optional depth of the output array
.   @sa  add, addWeighted, scaleAdd, Mat::convertTo'

    """
    return cv2.subtract(src1, src2, mask, dtype)


@rx_func()
def dilate(src: NDArray, kernel: NDArray, anchor: Tuple = (-1, -1), iterations: int = 1,
           borderType: ENUM_CV_BorderTypes = ENUM_CV_BorderTypes.BORDER_CONSTANT,) -> NDArray:
    """Dilates an image by using a specific structuring element.
    The function dilates the source image using the specified structuring element that determines the shape of a pixel neighborhood over which the maximum is taken:
    dst(x,y)=max(x′,y′):element(x′,y′)≠0src(x+x′,y+y′)
    The function supports the in-place mode. Dilation can be applied several ( iterations ) times. In case of multi-channel images, each channel is processed independently.
    """
    return cv2.dilate(src, kernel, None, anchor, iterations, borderType,)


@rx_func()
def erode(src: NDArray, kernel: NDArray, anchor: Tuple = (-1, -1), iterations: int = 1,
          borderType: ENUM_CV_BorderTypes = ENUM_CV_BorderTypes.BORDER_CONSTANT,) -> NDArray:
    """Erodes an image by using a specific structuring element.
The function erodes the source image using the specified structuring element that determines the shape of a pixel neighborhood over which the minimum is taken:
dst(x,y)=min(x′,y′):element(x′,y′)≠0src(x+x′,y+y′)
The function supports the in-place mode. Erosion can be applied several ( iterations ) times. In case of multi-channel images, each channel is processed independently."""
    return cv2.erode(src, kernel, None, anchor, iterations, borderType,)


@rx_func()
def matchTemplate(image: NDArray, templ: NDArray,
                  method: ENUM_CV_TemplateMatchModes = ENUM_CV_TemplateMatchModes.default,  mask: NDArray = None) -> NDArray:
    """Compares a template against overlapped image regions.
The function slides through image , compares the overlapped patches of size w×h against templ using the specified method and stores the comparison results in result . TemplateMatchModes describes the formulae for the available comparison methods ( I denotes image, T template, R result, M the optional mask ). The summation is done over template and/or the image patch: x′=0...w−1,y′=0...h−1
After the function finishes the comparison, the best matches can be found as global minimums (when TM_SQDIFF was used) or maximums (when TM_CCORR or TM_CCOEFF was used) using the minMaxLoc function. In case of a color image, template summation in the numerator and each sum in the denominator is done over all of the channels and separate mean values are used for each channel. That is, the function can take a color template and a color image. The result will still be a single-channel image, which is easier to analyze."""
    return cv2.matchTemplate(image, templ, method, None, mask)


@rx_func()
def contourArea(contour, oriented:bool=False):
    """
    Calculates a contour area.

The function computes a contour area. Similarly to moments , the area is computed using the Green formula. Thus, the returned area and the number of non-zero pixels, if you draw the contour using drawContours or fillPoly , can be different. Also, the function will most certainly give a wrong results for contours with self-intersections.
    """
    return  cv2.contourArea(contour,oriented)

@rx_func()
def convertScaleAbs(src: NDArray,  alpha:float=1., beta:float=0.) -> NDArray:
    'convertScaleAbs(src[, dst[, alpha[, beta]]]) -> dst\n.   @brief Scales, calculates absolute values, and converts the result to 8-bit.\n.   \n.   On each element of the input array, the function convertScaleAbs\n.   performs three operations sequentially: scaling, taking an absolute\n.   value, conversion to an unsigned 8-bit type:\n.   \\f[\\texttt{dst} (I)= \\texttt{saturate\\_cast<uchar>} (| \\texttt{src} (I)* \\texttt{alpha} +  \\texttt{beta} |)\\f]\n.   In case of multi-channel arrays, the function processes each channel\n.   independently. When the output is not 8-bit, the operation can be\n.   emulated by calling the Mat::convertTo method (or by using matrix\n.   expressions) and then by calculating an absolute value of the result.\n.   For example:\n.   @code{.cpp}\n.       Mat_<float> A(30,30);\n.       randu(A, Scalar(-100), Scalar(100));\n.       Mat_<float> B = A*5 + 3;\n.       B = abs(B);\n.       // Mat_<float> B = abs(A*5+3) will also do the job,\n.       // but it will allocate a temporary matrix\n.   @endcode\n.   @param src input array.\n.   @param dst output array.\n.   @param alpha optional scale factor.\n.   @param beta optional delta added to the scaled values.\n.   @sa  Mat::convertTo, cv::abs(const Mat&)'
    return cv2.convertScaleAbs(src, None, alpha, beta)

@rx_func()
def Canny(image: NDArray, threshold1:int, threshold2:int, apertureSize:int=3, L2gradient:bool=False) -> typing.Any:
    'Canny(image, threshold1, threshold2[, edges[, apertureSize[, L2gradient]]]) -> edges\n.   @brief Finds edges in an image using the Canny algorithm @cite Canny86 .\n.   \n.   The function finds edges in the input image and marks them in the output map edges using the\n.   Canny algorithm. The smallest value between threshold1 and threshold2 is used for edge linking. The\n.   largest value is used to find initial segments of strong edges. See\n.   <http://en.wikipedia.org/wiki/Canny_edge_detector>\n.   \n.   @param image 8-bit input image.\n.   @param edges output edge map; single channels 8-bit image, which has the same size as image .\n.   @param threshold1 first threshold for the hysteresis procedure.\n.   @param threshold2 second threshold for the hysteresis procedure.\n.   @param apertureSize aperture size for the Sobel operator.\n.   @param L2gradient a flag, indicating whether a more accurate \\f$L_2\\f$ norm\n.   \\f$=\\sqrt{(dI/dx)^2 + (dI/dy)^2}\\f$ should be used to calculate the image gradient magnitude (\n.   L2gradient=true ), or whether the default \\f$L_1\\f$ norm \\f$=|dI/dx|+|dI/dy|\\f$ is enough (\n.   L2gradient=false ).\n\n\n\nCanny(dx, dy, threshold1, threshold2[, edges[, L2gradient]]) -> edges\n.   \\overload\n.   \n.   Finds edges in an image using the Canny algorithm with custom image gradient.\n.   \n.   @param dx 16-bit x derivative of input image (CV_16SC1 or CV_16SC3).\n.   @param dy 16-bit y derivative of input image (same type as dx).\n.   @param edges output edge map; single channels 8-bit image, which has the same size as image .\n.   @param threshold1 first threshold for the hysteresis procedure.\n.   @param threshold2 second threshold for the hysteresis procedure.\n.   @param L2gradient a flag, indicating whether a more accurate \\f$L_2\\f$ norm\n.   \\f$=\\sqrt{(dI/dx)^2 + (dI/dy)^2}\\f$ should be used to calculate the image gradient magnitude (\n.   L2gradient=true ), or whether the default \\f$L_1\\f$ norm \\f$=|dI/dx|+|dI/dy|\\f$ is enough (\n.   L2gradient=false ).'
    return cv2.Canny(image,threshold1,threshold2,None,apertureSize,L2gradient)

if __name__ == "__main__":
    im = cv2.imread("static/result/139981248069776.png")
    # zeros = np.zeros((100,100),dtype='uint8')
    
    zeros = GaussianBlur(im, (5, 5), 0)
    # pdb.set_trace()
    cv2.imwrite('demo.jpg', zeros)
