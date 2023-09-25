import os
import pytest

from dcicutils.misc_utils import ignored, override_environ
from dcicutils.qa_utils import MockResponse
from unittest import mock
from .. import submission as submission_module
from dcicutils.creds_utils import SMaHTKeyManager
from ..scripts.resume_uploads import main as resume_uploads_main
from ..scripts import resume_uploads as resume_uploads_module
from .testing_helpers import system_exit_expected, argparse_errors_muffled


@pytest.mark.parametrize("keyfile", [None, "foo.bar"])
def test_resume_uploads_script(keyfile):

    def test_it(args_in, expect_exit_code, expect_called, expect_call_args=None):
        output = []
        with argparse_errors_muffled():
            with SMaHTKeyManager.default_keys_file_for_testing(keyfile):
                with mock.patch.object(resume_uploads_module, "print") as mock_print:
                    mock_print.side_effect = lambda *args: output.append(" ".join(args))
                    with mock.patch.object(resume_uploads_module, "resume_uploads") as mock_resume_uploads:
                        with system_exit_expected(exit_code=expect_exit_code):
                            key_manager = SMaHTKeyManager()
                            if keyfile:
                                assert key_manager.keys_file == keyfile
                            assert key_manager.keys_file == (keyfile or key_manager.KEYS_FILE)
                            resume_uploads_main(args_in)
                            raise AssertionError("resume_uploads_main should not exit normally.")  # pragma: no cover
                        assert mock_resume_uploads.call_count == (1 if expect_called else 0)
                        if expect_called:
                            assert mock_resume_uploads.called_with(**expect_call_args)
                        assert output == []

    test_it(args_in=[], expect_exit_code=2, expect_called=False)  # Missing args
    test_it(args_in=['some-guid'], expect_exit_code=0, expect_called=True, expect_call_args={
        'bundle_filename': None,
        'env': None,
        'server': None,
        'uuid': 'some-guid',
        'upload_folder': None,
        'no_query': False,
        'subfolders': False,
    })
    expect_call_args = {
        'bundle_filename': 'some.file',
        'env': None,
        'server': None,
        'uuid': 'some-guid',
        'upload_folder': None,
        'no_query': False,
        'subfolders': False,
    }
    test_it(args_in=['-b', 'some.file', 'some-guid'],
            expect_exit_code=0,
            expect_called=True,
            expect_call_args=expect_call_args)
    test_it(args_in=['some-guid', '-b', 'some.file'],
            expect_exit_code=0,
            expect_called=True,
            expect_call_args=expect_call_args)
    expect_call_args = {
        'bundle_filename': 'some.file',
        'env': 'some-env',
        'server': None,
        'uuid': 'some-guid',
        'upload_folder': None,
        'no_query': False,
        'subfolders': False,
    }
    test_it(args_in=['some-guid', '-b', 'some.file', '-e', 'some-env'],
            expect_exit_code=0,
            expect_called=True,
            expect_call_args=expect_call_args)
    test_it(args_in=['-b', 'some.file', '-e', 'some-env', 'some-guid'],
            expect_exit_code=0,
            expect_called=True,
            expect_call_args=expect_call_args)
    expect_call_args = {
        'bundle_filename': 'some.file',
        'env': 'some-env',
        'server': 'http://some.server',
        'uuid': 'some-guid',
        'upload_folder': None,
        'no_query': False,
        'subfolders': False,
    }
    test_it(args_in=['some-guid', '-b', 'some.file', '-e', 'some-env', '-s', 'http://some.server'],
            expect_exit_code=0,
            expect_called=True,
            expect_call_args=expect_call_args)
    test_it(args_in=['-b', 'some.file', '-e', 'some-env', '-s', 'http://some.server', 'some-guid'],
            expect_exit_code=0,
            expect_called=True,
            expect_call_args=expect_call_args)
    expect_call_args = {
        'bundle_filename': 'some.file',
        'env': 'some-env',
        'server': 'http://some.server',
        'uuid': 'some-guid',
        'upload_folder': 'a-folder',
        'no_query': False,
        'subfolders': False,
    }
    test_it(args_in=['some-guid', '-b', 'some.file', '-e', 'some-env', '-s', 'http://some.server', '-u', 'a-folder'],
            expect_exit_code=0,
            expect_called=True,
            expect_call_args=expect_call_args)
    test_it(args_in=['-b', 'some.file', '-e', 'some-env', '-s', 'http://some.server', 'some-guid',
                     '--upload_folder', 'a-folder'],
            expect_exit_code=0,
            expect_called=True,
            expect_call_args=expect_call_args)
    expect_call_args = {
        'bundle_filename': 'some.file',
        'env': None,
        'server': 'http://some.server',
        'uuid': 'some-guid',
        'upload_folder': 'a-folder',
        'no_query': True,
        'subfolders': False,
    }
    test_it(args_in=['some-guid', '-b', 'some.file', '-s', 'http://some.server', '-u', 'a-folder', '-nq'],
            expect_exit_code=0,
            expect_called=True,
            expect_call_args=expect_call_args)
    expect_call_args = {
        'bundle_filename': 'some.file',
        'env': None,
        'server': 'http://some.server',
        'uuid': 'some-guid',
        'upload_folder': 'a-folder',
        'no_query': True,
        'subfolders': True,
    }
    test_it(args_in=['some-guid', '-b', 'some.file', '-s', 'http://some.server', '-u', 'a-folder', '-nq', '-sf'],
            expect_exit_code=0,
            expect_called=True,
            expect_call_args=expect_call_args)


SAMPLE_UPLOAD_INFO = [
    {'uuid': 'df6e0e21-e575-4bd1-b81f-60d78e23a544', 'filename': 'f1.fastq.gz'},
    {'uuid': '7171b8fb-94e0-4c14-9a17-69fb5812e61f', 'filename': 'f2.fastq.gz'},
    {'uuid': '2567587d-9027-4e11-82f5-9e224a7c73be', 'filename': 'f3.fastq.gz'},
    {'uuid': '67912528-0c8a-484a-8f4b-3101f22b382a', 'filename': 'f4.fastq.gz'},
]

INGESTION_FRAGMENT_WITH_UPLOAD_INFO = {
    "additional_data": {
        "upload_info": SAMPLE_UPLOAD_INFO
    }
}


def test_c4_383_regression_action():
    """
    Check that bug C4-383 is really fixed.

    This bug involves resume_uploads not merging the uploaded file against the current directory
    when no bundle_filename or upload_folder is given. The present behavior is to merge against
    the parent directory.
    """
    output = []
    with override_environ(SMAHT_KEYS_FILE=None):
        with mock.patch.object(resume_uploads_module, "print") as mock_print:
            mock_print.side_effect = lambda *args: output.append(" ".join(args))
            # This is the directory we expect the uploaded file to get merged against.
            # We want to really run the code logic to make sure it does this,
            # so we have to mock out all the effects.
            current_dir = "/my/cur/dir"
            with mock.patch.object(os.path, "curdir", current_dir):
                with mock.patch.object(submission_module, "yes_or_no", return_value=True):
                    with mock.patch.object(submission_module, "upload_file_to_uuid") as mock_upload_file_to_uuid:
                        with mock.patch("requests.get") as mock_requests_get:

                            def mocked_requests_get(url, *args, **kwargs):
                                ignored(args, kwargs)
                                assert "ingestion-submissions" in url
                                return MockResponse(200, json=INGESTION_FRAGMENT_WITH_UPLOAD_INFO)

                            mock_requests_get.side_effect = mocked_requests_get
                            local_server = "http://localhost:8000"
                            fake_keydict = {
                                'key': 'my-key',
                                'secret': 'my-secret',
                                'server': local_server,
                            }
                            with mock.patch.object(SMaHTKeyManager, "get_keydict_for_server",
                                                   return_value=fake_keydict):
                                try:
                                    # Outside the call, we will always see the default filename for SMaHT keys
                                    # but inside the call, because of a decorator, the default might be different.
                                    # See additional test below.
                                    assert SMaHTKeyManager().keys_file == SMaHTKeyManager._default_keys_file()

                                    resume_uploads_main(["2eab76cd-666c-4b04-9335-22f9c6084303",
                                                         '--server', local_server])
                                except SystemExit as e:
                                    assert e.code == 0
                                joined_filename = os.path.join(current_dir, SAMPLE_UPLOAD_INFO[-1]['filename'])
                                # Make sure this is doing what we expect.
                                assert current_dir + "/" in joined_filename
                                # Make sure the inner upload actually uploads to the current dir.
                                mock_upload_file_to_uuid.assert_called_with(auth=fake_keydict,
                                                                            filename=joined_filename,
                                                                            uuid=SAMPLE_UPLOAD_INFO[-1]['uuid'])
                                assert output == []
