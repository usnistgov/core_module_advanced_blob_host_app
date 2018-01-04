""" Advanced blob host module views
"""
from core_main_app.components.blob import api as blob_api
from core_main_app.components.blob.models import Blob
from core_main_app.components.blob.utils import get_blob_download_uri
from core_module_advanced_blob_host_app.views.forms import URLForm
from core_module_blob_host_app.views.forms import BLOBHostForm
from core_module_blob_host_app.views.views import BlobHostModule
from core_parser_app.tools.modules.views.builtin.popup_module import PopupModule
from core_parser_app.tools.modules.views.module import AbstractModule


class AdvancedBlobHostModule(PopupModule):
    def __init__(self):
        """Initialize module

        """
        popup_content = AbstractModule.render_template('core_module_advanced_blob_host_app/advanced_blob_host.html',
                                                       {'url_form': URLForm(), 'file_form': BLOBHostForm()})

        PopupModule.__init__(self, popup_content=popup_content, button_label='Upload File',
                             scripts=['core_module_advanced_blob_host_app/js/advanced_blob_host.js'])

    def _retrieve_data(self, request):
        """ Return module display - GET method

        Args:
            request:

        Returns:

        """
        data = ''
        self.error = None
        if request.method == 'GET':
            if 'data' in request.GET:
                if len(request.GET['data']) > 0:
                    data = request.GET['data']
        elif request.method == 'POST':
            selected_option = request.POST['blob_form']
            if selected_option == "url":
                url_form = URLForm(request.POST)
                if url_form.is_valid():
                    data = url_form.data['url']
                else:
                    self.error = 'Enter a valid URL.'
            elif selected_option == "file":
                try:
                    # get file from request
                    uploaded_file = request.FILES['file']
                    # get filename from file
                    filename = uploaded_file.name
                    # get user id from request
                    user_id = str(request.user.id)

                    # create blob
                    blob = Blob(filename=filename, user_id=user_id)
                    # set blob file
                    blob.blob = uploaded_file
                    # save blob
                    blob_api.insert(blob)

                    # get download uri
                    data = get_blob_download_uri(blob, request)
                except:
                    self.error = 'An error occurred during the upload.'
        return data

    def _render_data(self, request):
        """ Return module's data rendering

        Args:
            request:

        Returns:

        """
        return BlobHostModule.render_blob_host_data(self.data, self.error)
