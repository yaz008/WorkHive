from project.configs import WorkHiveButton, FSASymbol
from project.libs.fsa import serializer
from project.libs.tgdraw import ButtonFactory


button_factory: ButtonFactory = ButtonFactory(serialize=serializer.serialize)


# Navigation:
button_factory.save(name=WorkHiveButton.Next, symbol=FSASymbol.Next)
button_factory.save(name=WorkHiveButton.NextErr, symbol=FSASymbol.Error)
button_factory.save(name=WorkHiveButton.Back, symbol=FSASymbol.Back)
button_factory.save(name=WorkHiveButton.Ok, symbol=FSASymbol.Ok)

# Actions:
button_factory.save(name=WorkHiveButton.Register, symbol=FSASymbol.Next)
button_factory.save(name=WorkHiveButton.Consent, symbol=FSASymbol.InputData)
# button_factory.save(name=WorkHiveButton.DeleteAccount, symbol=None)
# button_factory.save(name=WorkHiveButton.Post, symbol=None)
button_factory.save(name=WorkHiveButton.Add, symbol=FSASymbol.Add)
button_factory.save(name=WorkHiveButton.Delete, symbol=FSASymbol.Delete)
# button_factory.save(name=WorkHiveButton.Edit, symbol=None)
# button_factory.save(name=WorkHiveButton.Hide, symbol=None)
# button_factory.save(name=WorkHiveButton.ShowContact, symbol=None)
button_factory.save(name=WorkHiveButton.Accept, symbol=FSASymbol.Accept)
button_factory.save(name=WorkHiveButton.Decline, symbol=FSASymbol.Decline)
# button_factory.save(name=WorkHiveButton.Subscribe, symbol=None)
button_factory.save(name=WorkHiveButton.Publish, symbol=FSASymbol.Publish)
button_factory.save(name=WorkHiveButton.PublishErr, symbol=FSASymbol.Error)
button_factory.save(name=WorkHiveButton.Search, symbol=FSASymbol.Search)
button_factory.save(name=WorkHiveButton.Respond, symbol=FSASymbol.Respond)

# Menus:
button_factory.save(name=WorkHiveButton.Settings, symbol=FSASymbol.Settings)
# button_factory.save(name=WorkHiveButton.NotificationSettings, symbol=None)
button_factory.save(name=WorkHiveButton.Notifications, symbol=FSASymbol.Notifications)
button_factory.save(
    name=WorkHiveButton.NotificationsNew, symbol=FSASymbol.Notifications
)
button_factory.save(name=WorkHiveButton.MyPoints, symbol=FSASymbol.Points)
button_factory.save(name=WorkHiveButton.MyVacancies, symbol=FSASymbol.Vacancies)
button_factory.save(name=WorkHiveButton.MyResponds, symbol=FSASymbol.Responds)
button_factory.save(name=WorkHiveButton.Promocode, symbol=FSASymbol.Promocode)

# Other:
button_factory.save(name=WorkHiveButton.Worker, symbol=FSASymbol.InputData)
button_factory.save(name=WorkHiveButton.Owner, symbol=FSASymbol.InputData)
button_factory.save(name=WorkHiveButton.Language, symbol=FSASymbol.Language)
button_factory.save(name=WorkHiveButton.Subsrciption, symbol=FSASymbol.Subscription)
