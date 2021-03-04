FROM kbase/sdkbase2:python
MAINTAINER KBase Developer
# -----------------------------------------
# In this section, you can install any system dependencies required
# to run your App.  For instance, you could place an apt-get update or
# install line here, a git checkout to download code, or run any other
# installation scripts.

#here was one "dependency" for cobra that was officially distutil (ruamel-yaml)
#That wheel kept trying to uninstall to reinstall, which caused problems, so we use --ignore-installed

RUN rm -rf /miniconda/lib/python3.6/site-packages/numpy
RUN pip install --upgrade pip
RUN pip install cobra==0.15.2 --ignore-installed
RUN pip install networkx
RUN pip install cobrakbase==0.2.7 --ignore-installed

# -----------------------------------------

COPY ./ /kb/module
RUN mkdir -p /kb/module/work
RUN chmod -R a+rw /kb/module

WORKDIR /kb/module

RUN make all

COPY ./cobra_patch/model.py /miniconda/lib/python3.6/site-packages/cobra/core/model.py
COPY ./cobra_patch/solver.py /miniconda/lib/python3.6/site-packages/cobra/util/solver.py
COPY ./cobra_patch/sbml.py /miniconda/lib/python3.6/site-packages/cobra/io/sbml.py


ENTRYPOINT [ "./scripts/entrypoint.sh" ]

CMD [ ]
