# TODO: system modules: cloudpickle, loky
#
# Conditional build:
%bcond_with	doc	# Sphinx documentation (fails on missing examples???)
%bcond_without	tests	# unit tests
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

Summary:	Lightweight pipelining: using Python functions as pipeline jobs
Summary(pl.UTF-8):	Lekkie przetwarzanie potokowe przy użyciu funkcji pythonowych jako zadań
Name:		python-joblib
Version:	0.14.1
Release:	1
License:	BSD
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/joblib/
Source0:	https://files.pythonhosted.org/packages/source/j/joblib/joblib-%{version}.tar.gz
# Source0-md5:	182e6bc65681ea49a12775fdc86a8e24
URL:		https://pypi.org/project/joblib/
%if %{with python2}
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-pytest
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.4
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-pytest
BuildRequires:	python3-threadpoolctl
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python3-numpydoc
BuildRequires:	python3-sphinx_gallery
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python-modules >= 1:2.7
Conflicts:	python-numpy < 1:1.6.1
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Joblib is a set of tools to provide lightweight pipelining in Python.
In particular:
- transparent disk-caching of functions and lazy re-evaluation
   (memoize pattern)
- easy simple parallel computing
        
Joblib is optimized to be fast and robust on large data in particular
and has specific optimizations for numpy arrays. It is BSD-licensed.

%description -l pl.UTF-8
Joblib to zbiór narzędzi zapewniających lekkie przetwarzanie potokowe
w Pythonie. W szczególności:
- przezroczyste zapamiętywanie na dysku funkcji i leniwe ponowne
  wyliczanie (wzorzec memoize)
- łatwe, proste przetwarzanie równoległe

Biblioteka jest zoptymalizowana pod kątem szybkości i funkcjonalności,
w szczególności na dużych zbiorach danych; ma wyspecjalizowane
optymalizacje dla tablic numpy. Jest na licencji BSD.

%package -n python3-joblib
Summary:	Lightweight pipelining: using Python functions as pipeline jobs
Summary(pl.UTF-8):	Lekkie przetwarzanie potokowe przy użyciu funkcji pythonowych jako zadań
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.4
Conflicts:	python3-numpy < 1:1.6.1

%description -n python3-joblib
Joblib is a set of tools to provide lightweight pipelining in Python.
In particular:
- transparent disk-caching of functions and lazy re-evaluation
   (memoize pattern)
- easy simple parallel computing
        
Joblib is optimized to be fast and robust on large data in particular
and has specific optimizations for numpy arrays. It is BSD-licensed.

%description -n python3-joblib -l pl.UTF-8
Joblib to zbiór narzędzi zapewniających lekkie przetwarzanie potokowe
w Pythonie. W szczególności:
- przezroczyste zapamiętywanie na dysku funkcji i leniwe ponowne
  wyliczanie (wzorzec memoize)
- łatwe, proste przetwarzanie równoległe

Biblioteka jest zoptymalizowana pod kątem szybkości i funkcjonalności,
w szczególności na dużych zbiorach danych; ma wyspecjalizowane
optymalizacje dla tablic numpy. Jest na licencji BSD.

%package apidocs
Summary:	API documentation for Python joblib module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona joblib
Group:		Documentation

%description apidocs
API documentation for Python joblib module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona joblib.

%prep
%setup -q -n joblib-%{version}

%build
%if %{with python2}
%py_build

%if %{with tests}
%{__python} -m pytest joblib
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
# test_pool_memmap_with_big_offset seems unreliable with python3
%{__python3} -m pytest joblib -k 'not test_pool_memmap_with_big_offset'
%endif
%endif

%if %{with doc}
PYTHONPATH=$(pwd) \
%{__make} -C doc html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%{__rm} -r $RPM_BUILD_ROOT%{py_sitescriptdir}/joblib/test
%py_postclean
%endif

%if %{with python3}
%py3_install

%{__rm} -r $RPM_BUILD_ROOT%{py3_sitescriptdir}/joblib/test
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc LICENSE.txt README.rst
%{py_sitescriptdir}/joblib
%{py_sitescriptdir}/joblib-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-joblib
%defattr(644,root,root,755)
%doc LICENSE.txt README.rst
%{py3_sitescriptdir}/joblib
%{py3_sitescriptdir}/joblib-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc doc/_build/html/{_static,*.html,*.js}
%endif
