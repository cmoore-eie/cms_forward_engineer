def get_addto_template() -> str:
    template = """
  /**
   * Add item to the ${AttributeName} array. If the array is null the array will be initialised
   */
  public function addTo${AttributeName}(inItem : ${AttributeType}){
    if(${AttributeParent}.${AttributeName} == null){
      ${AttributeParent}.${AttributeName} = new ArrayList<${AttributeType}>().toTypedArray()
    }
  } 
"""
    return template


def get_removefrom_template() -> str:
    template = """
  /**
   * Remove item to the ${AttributeName} array.
   */
  public function removeFrom${AttributeName}(inItem : ${AttributeType}){
    if(${AttributeParent}.${AttributeName}.contains(inItem)){
      ${AttributeParent}.${AttributeName}.remove(inItem)
    }
  }
"""
    return template
