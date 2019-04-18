import setuptools


#with open("README.md", "r") as fh:
#    long_description = fh.read()

setuptools.setup(
    name='bcfr',
    version='1.0',
    scripts=['bcfr'] ,
    author="Zhongmin Han",
    author_email="hanzm_vp@163.com",
    description="Bin map constructer for RILs",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yxrose/bcfr",
    packages=setuptools.find_packages(),
    py_modules=['break_point', 'divbin', 'flow_across_df', 'haplotype_info_indv', 'implot', 'opdin_mc', 'df2ss', 'exgt', 'fmb', 'ibd_constraint', 'indv_hap_plot', 'maxparsi_mc', 'retrench'],
    install_requires=[
         'click','pandas','numpy','matplotlib'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Linux",
    ],
 )
