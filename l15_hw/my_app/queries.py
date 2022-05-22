from my_app import my_models


def db_get_sins(rows_view):
    data_sins = list(my_models.Sins.objects.all()[:rows_view])
    return data_sins


def db_post_sins(coffee_cups, date):
    new_row = my_models.Sins(coffee_cups=coffee_cups, date=date)
    new_row.save()
