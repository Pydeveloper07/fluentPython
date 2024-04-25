import asyncio
import random
import uuid
from typing import List

from app import models
from app.producers import publish_products, publish_variants
from app.shared.db_transaction import db_atomic
from app.shared.publisher import context, Context
from app.shared.utils import random_string

COMPANY_ID = 1586


async def update_variants():
    async for variants in variant_generator():
        bulk_data = []
        for variant in variants:
            if not variant.options:
                continue

            option = variant.options[0]
            option_1_name = "size"
            option_1_option = option.get("size")
            option_2_name = "color"
            option_2_option = option.get("color")

            if not all([option_1_option, option_2_option]):
                continue

            bulk_data.append(
                dict(
                    id=variant.id,
                    options=[
                        dict(name=option_1_name, option=option_1_option),
                        dict(name=option_2_name, option=option_2_option),
                    ]
                )
            )
        await models.Variant.objects().bulk_create_or_update(
            key="id",
            values=bulk_data
        )


async def variant_generator():
    page = 1
    limit = 2000
    while True:
        qs = models.Variant.objects()
        qs = qs.filter(models.Variant.company_id == COMPANY_ID)
        qs = qs.paginate(page, limit)
        variants = await qs.all()
        if not variants:
            break
        yield variants
        if len(variants) < limit:
            break
        page += 1


async def create_products():
    n = 100
    brands = await _get_brands(COMPANY_ID)
    categories = await _get_brands(COMPANY_ID)
    for i in range(1000):
        await _create(n, brands, categories)
        print(f"Created {(i+1) * n}/{1000 * n}...")
        await asyncio.sleep(2)


@context
@db_atomic
async def _create(n: int, brands: List[models.Brand], categories: List[models.Category], ctx: Context):
    bulk_data = []
    for i in range(n):
        guid = uuid.uuid4()
        brand = random.choice(brands)
        category = random.choice(categories)
        bulk_data.append(
            dict(
                guid=guid,
                name=str(guid),
                company_id=COMPANY_ID,
                category_id=category.id,
                brand_id=brand.id,
                type="physical",
                sku=guid.hex,
                barcode=guid.hex,
                supply_price=random.randint(100, 1000),
                retail_price=random.randint(100, 1000),
                maximum_retail_price=random.randint(100, 1000),
                description=random_string(30),
                width=random.randint(10, 50),
                height=random.randint(10, 50),
                length=random.randint(10, 50),
                dimension_unit="sm",
                weight=random.randint(10, 50),
                weight_unit="g",
                unit_of_measurement="unit",
                tags=[random_string(5), random_string(5), random_string(5)],
                strategy="fefo",
                is_multi_variant=True,
                track_serial_numbers=False,
                track_expiry_dates=random.choice([False, True]),
                track_batch_numbers=random.choice([False, True]),
                track_production_dates=random.choice([False, True]),
                barcoding_strategy="set",
                variant_count=5,
            )
        )
    err, products = await models.Product.objects().bulk_create(bulk_data)
    if err:
        raise Exception(err)
    await publish_products([p.guid for p in products], ctx, True)

    bulk_data = []
    for product in products:
        for i in range(5):
            guid = uuid.uuid4()
            bulk_data.append(
                dict(
                    company_id=product.company_id,
                    guid=guid,
                    product_id=product.id,
                    name=str(guid),
                    description=random_string(30),
                    sku=guid.hex,
                    barcode=guid.hex,
                    barcode_aliases=[guid.hex],
                    supply_price=random.randint(100, 1000),
                    retail_price=random.randint(100, 1000),
                    maximum_retail_price=random.randint(100, 1000),
                    width=random.randint(10, 50),
                    height=random.randint(10, 50),
                    length=random.randint(10, 50),
                    dimension_unit="sm",
                    weight=random.randint(10, 50),
                    weight_unit="g",
                    enabled=True,
                    options=_prepare_options(),
                    reorder_point=random.randint(50, 100),
                    reorder_quantity=random.randint(100, 200),
                    barcoding_strategy="set",
                    unit_of_measurement="unit",
                    pieces=random.randint(1, 5),
                )
            )
    err, variants = await models.Variant.objects().bulk_create(bulk_data)
    if err:
        raise Exception(err)

    await publish_variants([v.guid for v in variants], ctx, True)

    # Create Variant barcodes
    bulk_data = []
    for variant in variants:
        bulk_data.append(
            dict(
                company_id=variant.company_id,
                variant_id=variant.id,
                barcode=variant.barcode,
            )
        )
    err, _ = await models.VariantBarcode.objects().bulk_create(bulk_data)
    if err:
        raise Exception(err)

    # Create condition prices
    default_condition = await _get_default_condition()
    bulk_data = []
    for variant in variants:
        bulk_data.append(
            dict(
                condition_id=default_condition.id,
                variant_id=variant.id,
                supply_price=random.randint(100, 1000),
                retail_price=random.randint(100, 1000),
                maximum_retail_price=random.randint(100, 1000),
            )
        )
    err, _ = await models.ConditionPrice.objects().bulk_create(bulk_data)
    if err:
        raise Exception(err)

    # Create variant images
    bulk_data = []
    for variant in variants:
        bulk_data.append(
            dict(
                product_variant_id=variant.id,
                image_path=random_string(20),
            )
        )
    err, _ = await models.VariantImage.objects().bulk_create(bulk_data)
    if err:
        raise Exception(err)


async def _get_default_condition() -> models.Condition:
    qs = models.Condition.objects()
    qs = qs.filter(models.Condition.company_id == COMPANY_ID)
    qs = qs.filter(models.Condition.is_default == True)
    condition = await qs.get()
    return condition


def _prepare_options():
    colors = ['red', 'green', 'blue']
    sizes = ['S', 'M', 'L']
    return [dict(color=random.choice(colors), size=random.choice(sizes))]


async def _get_brands(company_id: int) -> List[models.Brand]:
    qs = models.Brand.objects()
    qs = qs.filter(models.Brand.company_id == company_id)
    brands = await qs.all()
    return brands


async def _get_categories(company_id: int) -> List[models.Category]:
    qs = models.Category.objects()
    qs = qs.filter(models.Category.company_id == company_id)
    categories = await qs.all()
    return categories
