from FlatFileProvider import FlatFileProvider

class ProviderFactory():
	def Create(self,configuration):
	
		# Todo: Create the provider from the configuration document.
		return FlatFileProvider(configuration)