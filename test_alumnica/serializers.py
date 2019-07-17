from rest_framework import serializers

from .models import TestColb, TestCard, QuestionColb, Alumno,\
            OptionColb, ParCard, OptionCard


class OptionColbSerializer(serializers.ModelSerializer):    
    class Meta:
        model  = OptionColb        
        fields = ('text', 'axis')


class QuestionColbSerializer(serializers.ModelSerializer):    
    options = OptionColbSerializer(source='optioncolb_set', many=True, read_only=True)    
    class Meta:
        model  = QuestionColb        
        fields = ('text','options')


class ColbSerializer(serializers.ModelSerializer):
    question = QuestionColbSerializer(read_only=True)    
    class Meta:
        model  = TestColb        
        fields = ('user',  'question', 'axis_obs', 'axis_abst', 'axis_exp_act', 'axis_exp_con')


class OptionCardSerializer(serializers.ModelSerializer):
    class Meta:
        model  = OptionCard        
        fields = ('text',  'type_moment', 'file_name')

class ParCardSerializer(serializers.ModelSerializer):
    options = OptionCardSerializer(many=True, read_only=True)    
    
    class Meta:
        model  = ParCard        
        fields = ('id', 'type_moment_selected',  'options',)

    

class CardSerializer(serializers.ModelSerializer):
    pares = ParCardSerializer(source='get_pares', many=True, read_only=False)    
    class Meta:
        model  = TestCard        
        fields = ('user', 'pares')

    def update(self, instance, validated_data):
        pares_data  = validated_data.pop('get_pares')
        pares = self.data['pares']        
        instance.id_last_set = pares[0].get('id')
        for i in range (len (pares)):
            
            p = ParCard.objects.get(pk=pares[i].get('id'))
            p.type_moment_selected = pares_data[i].get('type_moment_selected')
            p.save()   
        instance.save()        
        return instance



