from pydantic import BaseModel, Field


class ListQuery(BaseModel):
    page: int = Field(None, title="页数", description="指定查询的页数，譬如要获取第4页")
    page_size: int = Field(None, title="数据量", description="指定每页的数据量，譬如每页10条数据量")
    order_by: str = Field(None, title="排序规则", description="如果多个排序规则则用英语逗号隔开，譬如-id")