from django.shortcuts import render
from rest_framework.views import APIView
from .models import TestColb, TestCard, QuestionColb, Alumno, OptionCard, ParCard, typeMoment
from .serializers import ColbSerializer, QuestionColbSerializer,\
                    ParCardSerializer, OptionCardSerializer, CardSerializer
import itertools
from rest_framework.response import Response
from rest_framework import  status
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from collections import OrderedDict
import traceback 
# Create your views here.


class TestColbView(APIView):
    """
    Retrieve, update or delete a user instance.
    """
    
    def create_test(self, id_user):
        question = QuestionColb.objects.get(pk=1)
        user = Alumno.objects.get(pk=id_user)
        t = TestColb(question=question, user=user)
        t.save()
        print (t)
        return t


    def get_object(self, id_user):
        try:
            return TestColb.objects.get(user=id_user)
        except ObjectDoesNotExist:
            print ('se crea')
            return self.create_test(id_user)

    def parse_out (self, data):
        print (data)
        out_request = dict(data)        
        out_request['question'] = dict(data['question'])
        out_request['question']['options']={}
        for option in data['question'].get('options'):            
            out_request['question']['options'][option.get('id')] = dict (option)            
            out_request ['question']['options'][option.get('id')]['selected_order'] = None
        return out_request


    def parse_in (self, data):
        in_request = dict(data)
        options = []
        for option in data['question']['options'].values():            
            options.append(option)            
        in_request['question']['options'] = options
        return in_request


    def get(self, request,  id_user, format=None):
        try:
            
            test_colb = self.get_object(id_user)
            serializer = ColbSerializer(test_colb)            
            return Response( self.parse_out (serializer.data), status=status.HTTP_200_OK)
        except Exception as err:
            print (traceback.format_exc())            
            return Response({}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def put(self, request,  id_user, format=None):
        try:
            print ('in put colb')            
            test_colb = self.get_object(id_user)
            serializer = ColbSerializer(test_colb, self.parse_in(data=request.data))
            if serializer.is_valid():
                serializer.save()                
                return Response({},status=status.HTTP_200_OK)
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        except Exception as err:            
            print (traceback.format_exc())
            return Response({}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class TestCardView(APIView):
    """
    Retrieve, update or delete a user instance.
    """

    def create_set(self, pares_keys, test_card):
        for par_key in pares_keys:
            par_card = ParCard( test=test_card)
            par_card.save()
            par_card.options.add(OptionCard.objects.get(type_moment=par_key[0]))
            par_card.options.add(OptionCard.objects.get(type_moment=par_key[1]))
            par_card.save()                    
        return 



    def validate_draws (self, tuplas, test_card, afinnities_saved=[]):
        draws = []
        if 4 in afinnities_saved :
            max_affi = max(afinnities_saved) - 1 
        else:
            max_affi = 4
        for i in  range (len(tuplas) ):             
            if i == 0 and not tuplas[i][1] == tuplas[i+1][1]:
                setattr(test_card, 'affi_' + tuplas[i][0], max_affi)  
                max_affi = max_affi - 1
                continue           
            elif i == (len(tuplas)-1)  and not tuplas[i][1] == tuplas[i-1][1]:
                setattr(test_card, 'affi_' + tuplas[i][0], max_affi)  
                continue
            elif i > 0 and i < (len(tuplas)-1) and not (tuplas[i][1] == tuplas[i+1][1] or tuplas[i][1] == tuplas[i-1][1]):
                setattr(test_card, 'affi_' + tuplas[i][0], max_affi)  
                max_affi = max_affi - 1
                continue                                 
            else:                
                draws.append(tuplas[i][0])                
                max_affi = max_affi - 1
        
        test_card.save()         
        return draws
        


    def evaluate_test(self, test_card):
        responses={}
        values = [e.value for e in typeMoment]
        afinnities = []
        for v in values:
            affi_moment = getattr (test_card, 'affi_' + v)               
            if affi_moment ==0 :
                responses [v]=0 
            else:
                afinnities.append(affi_moment)                  
        
        results = list (map ( lambda x : x.type_moment_selected, test_card.get_last_set() ))        
        for r in results:
            responses[r]=responses[r] + 1

        #order results
        results_order = list ( {k: responses[k] for k in sorted(responses, key=responses.get, reverse=True)}.items())
        

        #validate results and generate combinations 
        draws = self.validate_draws(results_order, test_card, afinnities)
        if  draws != []:
            pares = list (itertools.combinations (draws,2))
            return self.create_set(pares , test_card)
        else:
            return []

    def create_test(self, id_user):  
        user = Alumno.objects.get(pk=id_user)
        values = [e.value for e in typeMoment]
        pares_keys = list (itertools.combinations (values,2))
        t = TestCard(user=user)        
        t.save()
        self.create_set(pares_keys, t)         
        return t
    
    def get_object(self, id_user):
        try:
            return TestCard.objects.get(user=id_user)
        except ObjectDoesNotExist: 
            return self.create_test(id_user)

    def parse_out (self, data):
        out_request = {'user': data['user']}
        for par in data['pares']:
            out_request [par.get('id')] = dict (par)
            out_request [par.get('id')]['options'] = {}
            out_request [par.get('id')]['current_pair'] = False
            for option in par.get('options'):                
                out_request [par.get('id')]['options'][option.get('id')] = dict(option)
        return out_request


    def parse_in (self, data):
        in_request = {'user': data.pop('user')}        
        pares = []
        for par in data.values():
            options = []
            for option in par['options'].values():
                options.append(option)
            par['options'] = options    
            pares.append (par)
        in_request ['pares'] = pares
        return in_request


    def get(self, request,  id_user, format=None):
        try:
            print ('in get card')
            test_colb = self.get_object(id_user)
            serializer = CardSerializer(test_colb) 
            print (serializer.data)           
            return Response(self.parse_out(serializer.data),status=status.HTTP_200_OK)
        except Exception as err:
            print (traceback.format_exc())
            return Response({}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def put(self, request,  id_user, format=None):
        try:            
        
            test_colb = self.get_object(id_user)
            serializer = CardSerializer(test_colb, self.parse_in(data=request.data))
            if serializer.is_valid():            
                test = serializer.save()
                new_set = self.evaluate_test(test)
                if  new_set != []:
                    serializer = CardSerializer(test_colb)            
                    return Response(self.parse_out( serializer.data),status=status.HTTP_200_OK)
                return Response({},status=status.HTTP_200_OK)
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        except Exception as err:
             print (traceback.format_exc())
             return Response({}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

