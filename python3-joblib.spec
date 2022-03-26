# TODO: system modules: cloudpickle, loky
#
# Conditional build:
%bcond_with	doc	# Sphinx documentation (fails on missing examples???)
%bcond_without	tests	# unit tests (some memmapping tests fail under load)

Summary:	Lightweight pipelining: using Python functions as pipeline jobs
Summary(pl.UTF-8):	Lekkie przetwarzanie potokowe przy użyciu funkcji pythonowych jako zadań
Name:		python3-joblib
Version:	0.15.1
Release:	3
License:	BSD
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/joblib/
Source0:	https://files.pythonhosted.org/packages/source/j/joblib/joblib-%{version}.tar.gz
# Source0-md5:	8760242e4719ca061aa7d5519a051e4b
URL:		https://pypi.org/project/joblib/
BuildRequires:	python3-modules >= 1:3.6
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-pytest
BuildRequires:	python3-threadpoolctl
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python3-numpydoc
BuildRequires:	python3-pandas
BuildRequires:	python3-sphinx_gallery
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python3-modules >= 1:3.6
Conflicts:	python3-numpy < 1:1.6.1
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
%py3_build

%if %{with tests}
%{__python3} -m pytest joblib
%endif

%if %{with doc}
PYTHONPATH=$(pwd) \
%{__make} -C doc html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%{__rm} -r $RPM_BUILD_ROOT%{py3_sitescriptdir}/joblib/test

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES.rst LICENSE.txt README.rst TODO.rst
%{py3_sitescriptdir}/joblib
%{py3_sitescriptdir}/joblib-%{version}-py*.egg-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc doc/_build/html/{_static,*.html,*.js}
%endif
