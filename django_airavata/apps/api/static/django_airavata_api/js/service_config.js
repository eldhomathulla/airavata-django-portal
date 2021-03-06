const post = "post";
const get = "get";
const put = "put";
const del = "delete";
/*
examples:

Generating Services based on the API view set
{
serviceName:{
url:'/example/api',
viewSet:true
}
}
Normal service configuration:
{
serviceName:{
serviceAction1:{
url:'/example/api/<look_up>',  # the <look_up> implies a path parameter lok_up
requestType:'post',
bodyParams:[...] # body parameter names for json parameter if body params id=s a list of array else an object with the param name for the body object
queryParams:[] # list query param names/ query param name to param name mapping


}
}
}
 */

export default {
    "GroupResourcePreference": {
        url: "/api/group-resource-profiles/",
        viewSet: true
    },
    "SharedEntitiesGroups": {
        url: "/api/shared/group/entities",
        viewSet: true
    },
    "Entities": {
        url: "/api/entities",
        viewSet: [{
            name:"create",
            pagination:true
        }]
    }
}