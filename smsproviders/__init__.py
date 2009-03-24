import WadjaProvider

class ProviderFactory():
	def Create(self,configuration):
	
		# Todo: Create the provider from the configuration document.
		return WadjaProvider.WadjaProvider(configuration)