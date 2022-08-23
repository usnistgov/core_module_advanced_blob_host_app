""" Advanced blob host module views
"""
from core_parser_app.tools.modules.views.builtin.popup_module import AbstractPopupModule
from core_parser_app.tools.modules.views.module import AbstractModule
from xml_utils.xsd_tree.operations.xml_entities import XmlEntities
from core_module_blob_host_app.views.forms import BLOBHostForm
from core_module_blob_host_app.views.views import BlobHostModule
from core_module_remote_blob_host_app.views.forms import URLForm
from core_module_advanced_blob_host_app.settings import AUTO_ESCAPE_XML_ENTITIES


class AdvancedBlobHostModule(AbstractPopupModule):
    """Advanced Blob Host Module"""

    def __init__(self):
        """Initialize module"""
        super().__init__(
            button_label="Upload File",
            scripts=[
                "core_parser_app/js/commons/file_uploader.js",
                "core_module_advanced_blob_host_app/js/advanced_blob_host.js",
            ],
            styles=["core_module_advanced_blob_host_app/css/advanced_blob_host.css"],
        )

    def _get_popup_content(self):
        """Return popup content

        Returns:

        """
        module_id = None

        if self.request:
            module_id = self.request.GET.get("module_id", None)

        # create the from and set an unique id
        blob_host_form = BLOBHostForm()
        blob_host_form.fields["file"].widget.attrs.update(
            {"id": "file-input-%s" % str(module_id)}
        )
        return AbstractModule.render_template(
            "core_module_advanced_blob_host_app/advanced_blob_host.html",
            {
                "url_form": URLForm(),
                "file_form": blob_host_form,
                "module_id": module_id,
            },
        )

    def _retrieve_data(self, request):
        """Return module display - GET method

        Args:
            request:

        Returns:

        """
        data = ""
        self.error = None
        data_xml_entities = XmlEntities()
        if (
            request.method == "GET"
            and "data" in request.GET
            and len(request.GET["data"]) > 0
        ):
            data = request.GET["data"]
        elif request.method == "POST":
            selected_option = request.POST["blob_form"]
            if selected_option == "url":
                url_form = URLForm(request.POST)
                if url_form.is_valid():
                    data = url_form.data["url"]
                else:
                    self.error = "Enter a valid URL."
            elif selected_option == "file":
                data = BlobHostModule().retrieve_post_data(request)

        return (
            data_xml_entities.escape_xml_entities(data)
            if AUTO_ESCAPE_XML_ENTITIES
            else data
        )

    def _render_data(self, request):
        """Return module's data rendering

        Args:
            request:

        Returns:

        """
        return BlobHostModule.render_blob_host_data(self.data, self.error)
