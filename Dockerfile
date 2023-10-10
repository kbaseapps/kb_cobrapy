FROM kbase/sdkbase2:python
MAINTAINER KBase Developer
# -----------------------------------------
# In this section, you can install any system dependencies required
# to run your App.  For instance, you could place an apt-get update or
# install line here, a git checkout to download code, or run any other
# installation scripts.

#here was one "dependency" for cobra that was officially distutil (ruamel-yaml)
#That wheel kept trying to uninstall to reinstall, which caused problems, so we use --ignore-installed
RUN apt-get update
RUN apt-get install -y gcc
RUN rm -rf /miniconda/lib/python3.6/site-packages/numpy
RUN rm -rf /miniconda/lib/python3.6/site-packages/ruamel*
RUN pip install --upgrade pip
RUN pip install --use-deprecated=legacy-resolver git+https://github.com/ModelSEED/ModelSEEDpy.git@2aa8a21525bb7006b720f423ca43b518a8632252
RUN pip install git+https://github.com/Fxe/cobrakbase.git@76c53a3448e8f86460af285ec87eb98372b8ae2b

# -----------------------------------------

COPY ./ /kb/module
RUN mkdir -p /kb/module/work
RUN chmod -R a+rw /kb/module

WORKDIR /kb/module

RUN make all

#COPY ./cobra_patch/model.py /miniconda/lib/python3.6/site-packages/cobra/core/model.py
#COPY ./cobra_patch/solver.py /miniconda/lib/python3.6/site-packages/cobra/util/solver.py
#COPY ./cobra_patch/sbml.py /miniconda/lib/python3.6/site-packages/cobra/io/sbml.py
COPY ./cobra_patch/configuration.py /miniconda/lib/python3.6/site-packages/cobra/core/configuration.py


ENTRYPOINT [ "./scripts/entrypoint.sh" ]

CMD [ ]
