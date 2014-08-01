module PixelatedService
  class Persona < Struct.new :ident, :name, :signature, :address
    def to_json
      {
        ident: self.ident,
        name: self.name,
        signature: self.signature,
        address: self.address
      }.to_json
    end
  end
end
