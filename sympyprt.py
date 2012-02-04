# -*- coding: UTF-8 -*-
#;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
#;;;    _____      _ ____  _____    _  _______ ____
#;;;   / ___/_____(_) __ \/ ___/    |/ / ___//  _/
#;;;   \__ \/ ___/ / / / /\__ \    |   /\__ \ / /
#;;;  ___/ / /__/ / /_/ /___/ /   /   |___/ // /
#;;; /____/\___/_/\____//____/   /_/_/____/___/
#;;;
#;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
#;;; $Id::                                                                    $
#;;; (C) 1998-2011 SciOS Scientific Operating Systems GmbH
#;;; http://www.scios.ch
#;;; FOR INTERNAL USE ONLY.
#;;; HEAD URL: $HeadURL::                                                     $
#;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
#;;; PROJECT ...............................: XSI
#;;; SUBPROJECT ............................: IPy compat
#;;; MODULE ................................: sympyprt.py
#;;; VERSION ...............................: 0.0.1
#;;; CREATION DATE .........................: 01.01.2000
#;;; MODIFICATION DATE .....................: 03.09.2011
#;;; PROGRAMMING LANGUAGE(S) ...............: Python
#;;; INTERPRETER/COMPILER ..................: Python 2.7 r27:82525
#;;; OPERATING SYSTEM(S) ...................: NT, Linux
#;;; CREATOR(S) ............................: pagani@scios.ch
#;;; CLIENT(S) .............................: public
#;;; URL ...................................: research.scios.ch
#;;; EMAIL .................................: xps@scios.ch
#;;; COPYRIGHT .............................: (C) 2011, SciOS GmbH
#;;; LICENSE ...............................: BSD (2)
#;;; DEPENDENCIES ..........................: IPython, LaTeX, Matplotlib
#;;; IMPORTS ...............................: see import list (code)
#;;; EXPORTS ...............................: %sympyprt
#;;; COMMENTS ..............................: -> SBCL 1.0.37, ANSI Common Lisp
#;;; SHORT DESCRIPTION .....................: SymPy LaTeX rendering in ipyQT
#;;; DOCUMENTATION PATH ....................: --
#;;; IDE ...................................: PyScripter V 2.4.2.2
#;;; SVN REVISION ..........................: $Rev::                          $
#;;; REVISION DATE .........................: $Date::                         $
#;;; REVISED BY ............................: $Author::                       $
#;;; REVISION HISTORY ......................: --
#;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
#-------------------------------------------------------------------------------
# Copyright 2011 SciOS Scientific Operating Systems GmbH. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY SciOS GMBH ''AS IS'' AND ANY EXPRESS OR IMPLIED
# WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO
# EVENT SHALL SciOS GMBH OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA,
# OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
# EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# The views and conclusions contained in the software and documentation are
# those of the authors and should not be interpreted as representing official
# policies, either expressed or implied, of SciOS.
#-------------------------------------------------------------------------------
#!/usr/bin/env python
 
 
"""
Usage: %load_ext sympyprt
 
This defines a magic command %sympyprt to control the TeX rendering:
  %sympyprt on|off ................... turn rendering on/off
  %sympyprt help ..................... show a help text
  %sympyprt use simple|mplib|latex ... set the rendering method
  %sympyprt <parameter> <value> ...... change a parameter
 
  Examples:
    %sympyprt fontsize 12        ;; set font size to 12 pt
    %sympyprt textcolor Red      ;; set text color to red
    %sympyprt backcolor Yellow   ;; set background color to yellow
                                    (default is Transparent)
    %sympyprt resolution 150     ;; set image resolution to 150 dpi
    %sympyprt imagsize bbox      ;; set image size to bbox = bounding box
                                    useful if offset is used
    %sympyprt imagesize tight    ;; no border around content (tight). This is
                                    the default.
    %sympyprt imagesize 2cm,3cm  ;; set the image size to 2x3 cm. There must
                                    be no whitespace within the dimension pair.
    %sympyprt offset -2cm,-1cm   ;; set the offset of the content within the
                                    image.
    %sympyprt reset config       ;; reset config to factory settings
    %sympyprt reset cache        ;; clear cache and delete all png files from
                                    the temp dir.
    %sympyprt matrix v           ;; set matrix border: p,v,b,V,B,small
    %sympyprt breqn on           ;; use the breqn package: on/off
    @sympyprt mode equation      ;; choose mode: inline, equation, equation*
 
Advanced usage:
  To access the internals do as follows (for example):
    from sympyprt import *
    cfg ...................... show configuration dictionary
                               values may be changed directly or with
                               the set_<parameter> functions.
    ObjCache ................. display the object cache (this is a dict)
                               full access
                               ObjCache[id(<sympy_object>)] -> TeX instance
                               -> can be re-rendered with different parameters
                               or deleted ....
                               There are also exposed manipulation functions
                               like putObj, getObj, hasObj, getPNG ...
    cfg_reset ................ reset the cfg dict to factory settings
 
    TeX0, TeX1, TeX2 ......... To test the rendering one can use the different
                               classes as follows, e.g.:
                               p = TeX2('$$\hbar^2$$') --> p
 
    Ex.
 
    for x in ObjCache.values():
      print x.tex # the TeX code of the object
 
    for x in ObjCache.values():
      print x.pngfile # the png file names in the temp dir
 
    from sympyprt import TeX2 as tex
    tex(r'This text was rendered with \LaTeX')
 
    Magic name:
    If one prefers another name for the %sympyprt magic, change the global
    variable _magic in the code below.
 
    Note: if the 'latex' method is used all the png images are stored in the
          user's temp directory. The LaTeX source and aux files will be cleared
          if cleanup is True but not the images. Either use the remove_pngfile
          function of the TeX2 class or clear the temp directory manually.
          NT: !dir %temp% -> show the content of the temp dir
 
          Many (if not most) objects are cached with its 'id'. When typing
          _n ([n] = IPy output number) a cached image will be shown. There
          are several methods to redraw the image:
          1. delete it from the cache
          2. get the instance from the cache and use its render() method
          3. delete the original object, so that simpy creates a new one (id)
 
Credit(s): based on ipython/extensions/sympyprinting.py by Brian Granger
"""
 
#;;;;;;;;;;;;
# Imports ;;;
#;;;;;;;;;;;;
import os, os.path
import re
import subprocess
 
from tempfile import NamedTemporaryFile
#from IPython.lib.latextools import latex_to_png
from latextools import latex_to_png
from matplotlib.mathtext import MathTextParser, MathtextBackendBitmap
from sympy import latex ,pretty
from StringIO import StringIO
from base64 import encodestring
 
#;;;;;;;;;;;;
# Globals ;;;
#;;;;;;;;;;;;
#
# ObjCache ........... dict to store TeX instances (format id : instance)
# cfg, _cfg .......... config dict for the TeX classes
# _active ............ bool to enable/disable rendering
# _use ............... the method to use for rendering: simple|mplib|latex
# _magic ............. name of the magic to switch sympyprt_active (on/off)
# _loaded ............ bool indicating whether extension is loaded
# _methods ........... list of rendering methods: simple|mplib|latex
# _params ............ list of user parameters (changeable via magic)
#
global ObjCache
global cfg, _cfg
global _active
global _use
global _magic
global _loaded
global _methods
global _params
 
 
 
#;;;;;;;;;;;;;;;;;
# Globals init ;;;
#;;;;;;;;;;;;;;;;;
ObjCache = {}
_active = True
_use = 'latex'
_magic = 'sympyprt'
_loaded = False
_methods = ['simple', 'mplib', 'latex']
_params = ['fontsize', 'resolution', 'imagesize', 'textcolor', 'backcolor',
           'offset', 'reset']
 
cfg = {'pt' : 11,
       'D'  : 120,
       'T'  : 'tight',
       'bg' : 'Transparent',
       'fg' : 'Black',
       'O'  : '0cm,0cm',
       'bd' : '0',
       'mode' : 'equation*',
       'matrix' : 'b',
       'breqn' : False,
       'cleanup' : True,
       'init_render' : True}
 
_cfg = cfg.copy()
 
#;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
# Functions to manipulate global vars ;;;
#;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
 
#
# ObjCache manipulation functions
#
def putObj(x, y): ObjCache[id(x)] = y
def getObj(x): return ObjCache[id(x)]
def hasObj(x): return ObjCache.has_key(id(x))
def getPNG(x): return getObj(x).png
def clearCache(): ObjCache.clear()
 
 
def set_fontsize(x): cfg['pt'] = x
def set_resolution(x): cfg['D'] = x
def set_imagesize(x): cfg['T'] = x
def set_backcolor(x): cfg['bg'] = x
def set_textcolor(x): cfg['fg'] = x
def set_imageoffset(x): cfg['O'] = x
def cfg_reset():
  global cfg
  cfg = _cfg.copy()
 
 
#;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
# Preps for the magic command ;;;
#;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
 
magic_help_text = """Usage: %<magicname> on | off | help | use <m> | <p> <v>
<m> : method
  simple ...... use IPython's latex_to_png (no options)
  mplib ....... use matplotlib (options: fontsize, textcolor, resolution)
  latex ....... use LaTeX (required). Options are: fontsize, textcolor,
                resolution, imagesize, backcolor and offset.
 
<p> : parameter, <v> : value
  fontsize .... set the fontsize (unit: pt), <v> = Integer
  resolution .. set the resolution (unit: dpi), <v> = Integer
  imagesize ... set the image size. <v> may be tight, bbox or
                a comma separated dimension pair: e.g. 4cm,2cm
                (No whitespace between characters!)
  textcolor.... set the foreground color. <v> = colorname, e.g. Red, Blue
  backcolor ... set the background color. <v> = colorname, e.g. Yellow
  offset ...... offset for image content. <v> = a comma separated dimension
                pair: e.g. -1cm,-2cm (No whitespace between characters!)
  mode ........ <v> = inline, equation, equation*
  matrix ...... matrix type: <v> = p,v,b,V,B,small (as in LaTeX: <v>matrix)
  breqn ....... use the breqn package: <v> = on/off
  reset ....... <v> = config|cache; config: reset the cfg to factory settings
                cache: clear the cache and remove the png files from temp.
*EOI*
"""
 
 
#
# Function to switch the sympyprt_active variable True/False and printing a
# help text.
#
def _fswitch(arg):
  global _active
  global _magic
  d = {True : 'on', False : 'off'}
  if arg == 'on':
    _active = True
  elif arg == 'off':
    _active = False
  elif arg == 'help':
    print magic_help_text
  else:
    print 'Usage: %s on|off|help|use <m>|<p> <v>' % ('%' + _magic)
    print 'Current state: %s' % d[_active]
 
#
# Function  to set the render method
#
def _fmethod(arg):
  global _use
  global _methods
  if arg in _methods:
    _use = arg
  else:
    print 'Usage: %s use %s' % (('%' + _magic), '|'.join(_methods))
    print 'Current method: %s' % _use
 
#
# Function to set parameters
#
def _fparams(p, v):
  global _magic, _params, ObjCache
  if p == 'fontsize':
    cfg['pt'] = int(v)
  elif p == 'resolution':
    cfg['D'] = int(v)
  elif p == 'imagesize':
    cfg['T'] = v
  elif p == 'textcolor':
    cfg['fg'] = v.capitalize()
  elif p == 'backcolor':
    cfg['bg'] = v.capitalize()
  elif p == 'offset':
    cfg['O'] = v
  elif p == 'matrix':
    cfg['matrix'] = v
  elif p == 'mode':
    cfg['mode'] = v
  elif p == 'breqn':
    d = {'on':True, 'off':False}
    if v  in d.keys():
      cfg['breqn'] = d[v]
  elif p == 'show':
    if v == 'config':
      for k in cfg:
        print k," : ", cfg[k]
  elif p == 'reset':
    if v == 'config':
      cfg_reset()
    elif v == 'cache':
      for x in ObjCache.values():
        os.remove(x.pngfile)
      clearCache()
  else:
    print 'Usage: %s %s <value>' % (('%' + _magic), '|'.join(_params))
 
 
def _fmagic(self, *args):
  a = args[0].split()
  l = len(a)
  if l == 0:
    _fswitch('none')
  elif l == 1:
    _fswitch(a[0])
  elif l == 2:
    if a[0] == 'use':
      _fmethod(a[1])
    else:
      _fparams(a[0], a[1])
 
 
#;;;;;;;;;;;;;;;
# IPy magics ;;;
#;;;;;;;;;;;;;;;
 
#
# Define an IPython magic command: %sympyprt on|off ...
#
try:
  ip = get_ipython()
  ip.define_magic(_magic, _fmagic)
except:
  pass
 
 
#;;;;;;;;;;;;;;;
# Class TeX0 ;;;
#;;;;;;;;;;;;;;;
class TeX0():
  """
  Render TeX code with IPython lib latextools (not many options here ;)
  """
  def __init__(self, s, encode = False):
    self.png = latex_to_png(s, encode)
  def _repr_png_(self):
    return self.png
 
 
#;;;;;;;;;;;;;;;
# Class TeX1 ;;;
#;;;;;;;;;;;;;;;
class TeX1():
  """
  Render TeX code with matplotlib mathtext. Doesn't need a LaTeX installation.
  @texstr ........ TeX code as string
  @color ......... Font color
  @dpi ........... Resolution (dots per inch)
  @fontsize ...... Font size
  @enocde ........ Enocde base64
  @init_render ... Render the PNG image when creating an instance.
                   If 'False' one has to call the render method explicitly.
  """
  def __init__(self, texstr, encode = False):
 
    self.texstr = texstr
    self.color = cfg['fg']
    self.dpi = cfg['D']
    self.fontsize = cfg['pt']
    self.encode = encode
    self.init_render = cfg['init_render']
    self.png = None
 
    if self.init_render:
      self.render()
 
  def render(self):
    self.mtp = MathTextParser('bitmap')
    f = StringIO()
    self.mtp.to_png(f, self.texstr, self.color, self.dpi, self.fontsize)
    bin_data = f.getvalue()
    if self.encode:
      bin_data = encodestring(bin_data)
    self.png = bin_data
    f.close()
 
  def set_texstr(self, texstr):
    self.texstr = texstr
    self.render()
 
  def set_color(self, color):
    self.color = color
    self.render()
 
  def set_dpi(self, dpi):
    self.dpi = dpi
    self.render()
 
  def set_fontsize(self, fontsize):
    self.fontsize = fontsize
    self.render()
 
  def set_encode(self, encode):
    self.encode = encode
    self.render()
 
  def _repr_png_(self):
    return self.png
 
 
#;;;;;;;;;;;;;;;
# Class TeX2 ;;;
#;;;;;;;;;;;;;;;
class TeX2():
  """
  Convert TeX code to a PNG image via dvi using the 'dvipng' command.
  Credit: dvipng 1.XX Copyright 2002-2008 Jan-Ake Larsson
  Details: http://www.nongnu.org/dvipng/dvipng_4.html
 
    D = #         Output resolution
    O = c         Image offset
    T = c         Image size (also accepts '-T bbox' and '-T tight')
 
    bg = s        Background color (TeX-style color or 'Transparent')
    fg = s        Foreground color (TeX-style color)
    bd = #        Transparent border width in dots
    bd = s        Transparent border fallback color (TeX-style color)
 
    pt = #        Font size set in \documentstyle[#pt]
 
    cleanup = True | False ... removes .aux, .tex, .log and .dvi files.
    init_render = True | False ... render image when instance is created.
    latex_template = Tex preambel + begin/end{document}
 
     # = number   f = file   s = string  * = suffix, '0' to turn off
     c = comma-separated dimension pair (e.g., 3.2in,-32.1cm)
     color-spec: ex. rgb 1.0 0.0 0.0 , 'White', 'transparent' ...
 
    Return value: 'False' if an error occurs (check the variables
      latex_log, dvipng_log respectively).
 
    It is up to the user to delete/copy/move the PNG file from its
    temporary location.
  """
 
  def __init__(self, tex):
 
    self.tex = tex
    self.pt = cfg['pt']
    self.D = cfg['D']
    self.T = cfg['T']
    self.bg = cfg['bg']
    self.fg = cfg['fg']
    self.O = cfg['O']
    self.bd = cfg['bd']
    self.cleanup = cfg['cleanup']
    self.init_render = cfg['init_render']
 
    # Executables
    self.latex_exe = 'latex'
    self.dvipng_exe = 'dvipng'
 
    # Log (subprocess/communicate output in case of errors)
    self.log = None
 
    # Default template (don't overwrite at runtime)
    self.default_template = r'''\documentclass[%ipt]{article}
      \usepackage{amssymb,amsmath,bm,color}
      \usepackage[latin1]{inputenc}
      \usepackage{flexisym}
      \usepackage{breqn}
      \pagestyle{empty}
      \begin{document}
      %s
      \end{document}'''
 
    # Dvipng options template
    self.dvipng_opt_template = "-T %s -D %i -bg %s -fg %s -O %s -bd %s"
 
    # Use the default template (may be overwritten at runtime)
    self.latex_template = self.default_template
 
    # The image file
    self.pngfile = None
 
    # The image string (bin code)
    self.png = None
 
    # Render now or later?
    if self.init_render:
      self.render()
 
  def render(self):
 
    # Create a named temporary file for the TeX source code
    tex_file = NamedTemporaryFile(suffix = ".tex", delete = False)
    tex_file_name = tex_file.name
    tmp_file_base = tex_file_name[:-4]
 
    # Create the TeX source (template % (font_size, tex_string)
    tex_input = self.latex_template % (self.pt, self.tex)
 
    # Write TeX input to temp file and close it
    tex_file.write(tex_input)
    tex_file.close()
 
    # LaTeX process
    opt = "-output-directory=" + os.path.dirname(tex_file_name)
    cmd = '%s -halt-on-error %s %s' %  (self.latex_exe, opt, tex_file_name)
    latex = subprocess.Popen(cmd, shell = True, stdout = subprocess.PIPE)
 
    # Read stdout/stderr & handle errors
    latex_log = latex.communicate()
 
    if  latex.returncode != 0:
      print latex_log
      self.log = latex_log
      try:
        self.remove_tempfiles(tmp_file_base)
      except:
        pass
      return False
 
    # Run conversion (dvi -> png)
    pngfile = tmp_file_base + ".png"
    dvifile = tmp_file_base + ".dvi"
    val = (self.T, self.D, self.bg, self.fg, self.O, self.bd)
    opt = self.dvipng_opt_template % val
 
    cmd = '%s %s -o %s %s' % (self.dvipng_exe, opt, pngfile, dvifile)
    dvipng = subprocess.Popen(cmd, shell = True, stdout = subprocess.PIPE)
 
    # Read stdout/stderr & handle errors
    dvipng_log = dvipng.communicate()
 
    if dvipng.returncode != 0:
      print dvipng_log, opt
      self.log = dvipng_log
      try:
        self.remove_tempfiles(tmp_file_base)
      except:
        pass
      return False
 
    # Cleanup?
    if self.cleanup:
      self.remove_tempfiles(tmp_file_base)
 
    # Set png image path
    self.pngfile = pngfile
 
    # Read the image (use binary read)
    f = open(self.pngfile, 'rb')
    self.png = f.read()
    f.close()
 
  def set_texstr(self, texstr):
    """
    Change the TeX input string.
    """
    self.tex = texstr
    self.render()
 
  def set_color(self, fore_color, back_color):
    """
    Change fore/back color.
    """
    self.fg = fore_color
    self.bg = back_color
    self.render()
 
  def set_dpi(self, dpi):
    """
    Change image resolution (dots per inch).
    """
    self.D = dpi
    self.render()
 
  def set_fontsize(self, fontsize):
    """
    Change font size (pt; in preambel)
    """
    self.pt = fontsize
    self.render()
 
  def set_imagesize(self, fontsize):
    """
    Change image size (dimension pair, bbox or tight)
    """
    self.T = imagesize
    self.render()
 
  def remove_tempfiles(self, base_name):
    """
    Remove temp files.
    """
    suffixes = ['dvi', 'aux', 'log', 'tex']
    to_remove = map(lambda s: base_name + '.' + s, suffixes)
 
    for item in to_remove:
      os.remove(item)
 
  def remove_pngfile(self):
    """
    Remove the image file.
    """
    os.remove(self.pngfile)
 
  def _repr_png_(self):
    """
    Return the png image string (bin code).
    """
    return self.png
 
 
#;;;;;;;;;;;;;;;;;;;;;;;
# Printing functions ;;;
#;;;;;;;;;;;;;;;;;;;;;;;
 
def print_basic_unicode(o, p, cycle):
    """A function to pretty print sympy Basic objects."""
    if cycle:
        return p.text('Basic(...)')
    out = pretty(o, use_unicode=True)
    if '\n' in out:
        p.text(u'\n')
    p.text(out)
 
def print_png0(obj):
  """
  Display sympy expression using TeX0.
  """
  global _active
  if not _active: return None
  s = latex(obj, mode = 'inline')
  # mathtext does not understand certain latex flags, so we try to replace
  # them with suitable subs.
  s = s.replace('\\operatorname','')
  s = s.replace('\\overline', '\\bar')
  png = TeX0(s).png
  return png
 
def print_png1(obj):
  """
  Display sympy expression using TeX1.
  """
  global _active
  if not _active: return None
  s = latex(obj, mode = 'inline')
  # mathtext does not understand certain latex flags, so we try to replace
  # them with suitable subs.
  s = s.replace('\\operatorname','')
  s = s.replace('\\overline', '\\bar')
  png = TeX1(s).png
  return png
 
 
def print_png2(self):
  """
  Display sympy expression using TeX2.
  """
  global _active
  if not _active: return None
  if hasObj(self):
    return getPNG(self)
  else:
    try:
      s = latex(self, mode = '%s' % cfg['mode'])
      #s = s.replace('smallmatrix','bmatrix') #v, V, b, B, p
      s = s.replace('\\left(\\begin{smallmatrix}',
                    '\\begin{%smatrix}' % cfg['matrix'])
      s = s.replace('\\end{smallmatrix}\\right)',
                    '\\end{%smatrix}' % cfg['matrix'])
      # breqn
      if cfg['breqn']:
        s = s.replace('{equation*}', '{dmath*}')
 
      repr_obj = TeX2(s)
      putObj(self, repr_obj)
      return repr_obj.png
    except:
      return None
 
 
def print_png(obj):
  """
  Depending on method (_use) activate the corresponding function.
  """
  global _use
  if _use == 'simple':
    return print_png0(obj)
  elif _use == 'mplib':
    return print_png1(obj)
  elif _use == 'latex':
    return print_png2(obj)
  else:
    return None
 
#;;;;;;;;;;;;;;;;;
# IPy Extension;;;
#;;;;;;;;;;;;;;;;;
 
def load_ipython_extension(ip):
  """
  Load the extension in IPython.
  """
  global _loaded
  if not _loaded:
    plaintext_formatter = ip.display_formatter.formatters['text/plain']
 
    for cls in (object, tuple, list, set, frozenset, dict, str):
        plaintext_formatter.for_type(cls, print_basic_unicode)
 
    plaintext_formatter.for_type_by_name('sympy.core.basic', 'Basic',
      print_basic_unicode)
    plaintext_formatter.for_type_by_name('sympy.matrices.matrices',
      'Matrix', print_basic_unicode)
 
    png_formatter = ip.display_formatter.formatters['image/png']
    png_formatter.for_type_by_name('sympy.matrices.matrices','Matrix', print_png)
    png_formatter.for_type_by_name('sympy.core.basic', 'Basic', print_png)
 
    _loaded = True
 
 
 
 
 
 
 
def main():
    pass
 
if __name__ == '__main__':
    main()


