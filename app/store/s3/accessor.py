import typing

from aiobotocore import get_session
from aiobotocore.paginate import AioPaginator
from aiobotocore.session import AioSession
from aiohttp import BodyPartReader

from drive_server.app.api.utils.part_iterator import reader_iterator
from drive_server.app.base.connect_accessor import ConnectAccessor
from drive_server.app.config.dataclasses import S3ConfigSection
from drive_server.app.store.s3.multipart_uploader import MultipartUploader


class S3Accessor(ConnectAccessor):
    def _init_(self):
        self._session: AioSession = get_session()
        self.config: S3ConfigSection = self.app.config.s3

    async def _connect(self) -> None:
        async with self._session.create_client('s3', **self.config.credentials) as client:
            await client.list_buckets()

    async def upload(self, key: str, reader: BodyPartReader, upload_callback: typing.Optional[callable] = None):
        async with self._session.create_client('s3', **self.config.credentials) as client:
            async with MultipartUploader(client=client, config=self.config, key=key) as mpu:
                async for chunk in reader_iterator(reader):
                    await mpu.upload_part(chunk)
                    if upload_callback:
                        await upload_callback(mpu.uploaded_size)

    async def delete_object(self, key: str) -> None:
        async with self._session.create_client('s3', **self.config.credentials) as client:
            await client.delete_object(Key=key, Bucket=self.config.bucket_name)


    async def list_objects(self) -> list[dict]:
        async with self._session.create_client('s3', **self.config.credentials) as client:
            f: dict = await client.list_objects(Bucket=self.config.bucket_name)
            return f.get("Contents")

