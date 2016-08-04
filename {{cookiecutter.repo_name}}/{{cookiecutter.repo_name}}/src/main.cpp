#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/eigen.h>

Eigen::VectorXd add(const Eigen::VectorXd& a, const Eigen::VectorXd& b) {
    return a + b;
}

Eigen::VectorXd subtract(const Eigen::VectorXd& a, const Eigen::VectorXd& b) {
    return a - b;
}

namespace py = pybind11;

PYBIND11_PLUGIN(ext) {
    py::module m("ext", R"pbdoc(
        Pybind11 example plugin
        -----------------------
        .. currentmodule:: {{ cookiecutter.repo_name }}.ext
        .. autosummary::
           :toctree: _generate
           add
           subtract
    )pbdoc");

    m.def("add", &add, R"pbdoc(
        Add two vectors
    )pbdoc");

    m.def("subtract", &subtract, R"pbdoc(
        Subtract two vectors
    )pbdoc");

#ifdef VERSION_INFO
    m.attr("__version__") = py::str(VERSION_INFO);
#else
    m.attr("__version__") = py::str("dev");
#endif

    return m.ptr();
}
